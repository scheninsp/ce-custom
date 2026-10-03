// 功能：从 Ghidra 程序导出 Refresh 的静态可达调用图，供项目 AI 读取。
// 入参：输出目录、函数命名表、可选的 discover；返回：JSON 图、反汇编和分片伪代码。
// @category Victoria3

import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.address.AddressSetView;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.util.task.TaskMonitor;
import com.google.gson.GsonBuilder;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ExportRefreshTree extends GhidraScript {
    private final Map<String, Map<String, Object>> nodes = new LinkedHashMap<>();
    private final List<Map<String, Object>> edges = new ArrayList<>();
    private final Map<String, String> names = new HashMap<>();
    private Address imageBase;
    private Path output;
    private Path codeOutput;
    private final NavigableMap<Long, Long> runtimeRanges = new TreeMap<>();

    // 功能：执行静态图遍历和可恢复导出；入参：脚本参数；返回：无。
    @Override public void run() throws Exception {
        String[] args = getScriptArgs();
        output = Paths.get(args[0]);
        codeOutput = Paths.get(args[1]);
        Files.createDirectories(output);
        Files.createDirectories(codeOutput);
        imageBase = currentProgram.getImageBase();
        MemoryBlock pdata = currentProgram.getMemory().getBlock(".pdata");
        if (pdata != null) {
            for (long offset = 0; offset + 12 <= pdata.getSize(); offset += 12) {
                long begin = Integer.toUnsignedLong(currentProgram.getMemory().getInt(pdata.getStart().add(offset)));
                long end = Integer.toUnsignedLong(currentProgram.getMemory().getInt(pdata.getStart().add(offset + 4)));
                if (begin > 0 && end > begin) runtimeRanges.put(begin, end);
            }
        }
        if (args.length > 2 && Files.exists(Paths.get(args[2]))) {
            for (String line : Files.readAllLines(Paths.get(args[2]), StandardCharsets.UTF_8)) {
                String[] pair = line.trim().split("\\s+", 2);
                if (pair.length == 2) names.put(pair[0].toUpperCase(), pair[1]);
            }
        }
        Function root = currentProgram.getFunctionManager().getFunctionAt(imageBase.add(0x11FBDA0L));
        if (root == null) throw new IllegalStateException("Root function missing at " + imageBase.add(0x11FBDA0L));
        println("ROOT " + root.getEntryPoint() + " BASE " + imageBase);
        ArrayDeque<Function> queue = new ArrayDeque<>();
        Map<Address, Function> found = new LinkedHashMap<>();
        Map<Address, Integer> depths = new HashMap<>();
        queue.add(root); found.put(root.getEntryPoint(), root); depths.put(root.getEntryPoint(), 0);
        while (!queue.isEmpty()) {
            monitor.checkCancelled();
            Function fn = queue.remove();
            prepareFunction(fn);
            String id = rva(fn.getEntryPoint());
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("rva", id); node.put("address", fn.getEntryPoint().toString());
            node.put("ghidra_name", fn.getName()); node.put("name", names.getOrDefault(id, fn.getName()));
            node.put("depth", depths.get(fn.getEntryPoint())); node.put("external", fn.isExternal());
            node.put("body", fn.getBody().toString());
            nodes.put(id, node);
            if (fn.isExternal()) continue;
            InstructionIterator instructions = currentProgram.getListing().getInstructions(fn.getBody(), true);
            while (instructions.hasNext()) {
                Instruction ins = instructions.next();
                boolean call = ins.getFlowType().isCall();
                boolean jump = ins.getFlowType().isJump();
                if (!call && !jump) continue;
                LinkedHashSet<Address> targets = new LinkedHashSet<>();
                targets.addAll(Arrays.asList(ins.getFlows()));
                for (Reference ref : ins.getReferencesFrom()) {
                    if (ref.getReferenceType().isCall() || ref.getReferenceType().isJump()) targets.add(ref.getToAddress());
                    if (ins.getFlowType().isComputed() && ref.getReferenceType().isData()) {
                        Function imported = currentProgram.getFunctionManager().getReferencedFunction(ref.getToAddress());
                        if (imported != null) targets.add(imported.getEntryPoint());
                        for (Reference pointer : currentProgram.getReferenceManager().getReferencesFrom(ref.getToAddress())) {
                            if (pointer.isExternalReference()) targets.add(pointer.getToAddress());
                        }
                    }
                }
                boolean resolved = false;
                for (Address target : targets) {
                    if (jump && fn.getBody().contains(target)) continue;
                    Function child = currentProgram.getFunctionManager().getFunctionAt(target);
                    if (child == null && target.isExternalAddress()) {
                        ExternalLocation external = currentProgram.getExternalManager().getExternalLocation(
                            currentProgram.getSymbolTable().getPrimarySymbol(target));
                        if (external != null) child = external.createFunction();
                    }
                    if (child == null) child = currentProgram.getFunctionManager().getFunctionContaining(target);
                    if (child == null && currentProgram.getMemory().getExecuteSet().contains(target)) {
                        child = createFunction(target, null);
                    }
                    Map<String, Object> edge = new LinkedHashMap<>();
                    edge.put("from", id); edge.put("site", rva(ins.getAddress()));
                    edge.put("kind", call ? "call" : "tail_or_external_jump");
                    edge.put("instruction", ins.toString()); edge.put("target_address", target.toString());
                    edge.put("to", child == null ? null : rva(child.getEntryPoint()));
                    edges.add(edge); resolved = true;
                    if (child != null && !found.containsKey(child.getEntryPoint())) {
                        found.put(child.getEntryPoint(), child);
                        depths.put(child.getEntryPoint(), depths.get(fn.getEntryPoint()) + 1);
                        queue.add(child);
                    }
                }
                if (!resolved && (call || ins.getFlowType().isComputed())) {
                    Map<String, Object> edge = new LinkedHashMap<>();
                    edge.put("from", id); edge.put("site", rva(ins.getAddress()));
                    edge.put("kind", call ? "unresolved_indirect_call" : "unresolved_computed_jump"); edge.put("instruction", ins.toString());
                    edge.put("to", null); edges.add(edge);
                }
            }
            if (nodes.size() % 100 == 0) println("DISCOVER " + nodes.size() + " QUEUED " + queue.size());
        }
        Map<String, Object> graph = new LinkedHashMap<>();
        graph.put("program", currentProgram.getName()); graph.put("executable_path", currentProgram.getExecutablePath());
        graph.put("executable_sha256", currentProgram.getExecutableSHA256());
        graph.put("image_base", imageBase.toString()); graph.put("root_rva", "11FBDA0");
        graph.put("ghidra_version", ghidra.framework.Application.getApplicationVersion());
        graph.put("nodes", nodes.values()); graph.put("edges", edges);
        write(output.resolve("callgraph.json"), new GsonBuilder().setPrettyPrinting().create().toJson(graph));
        println("GRAPH_DONE FUNCTIONS " + nodes.size() + " EDGES " + edges.size());
        if (args.length > 3 && args[3].equals("discover")) return;
        // 沿用已存在的分析名称，仅改变一次性副本中的标签。
        for (Function fn : found.values()) {
            String name = names.get(rva(fn.getEntryPoint()));
            if (name != null && !fn.isExternal()) fn.setName(name, SourceType.USER_DEFINED);
        }
        ExecutorService pool = Executors.newFixedThreadPool(4);
        AtomicInteger done = new AtomicInteger();
        List<Future<?>> tasks = new ArrayList<>();
        final int total = found.size();
        for (Function fn : found.values()) {
            if (fn.isExternal()) { nodes.get(rva(fn.getEntryPoint())).put("status", "external_no_body"); continue; }
            tasks.add(pool.submit(() -> {
                String id = rva(fn.getEntryPoint());
                Path statusFile = output.resolve("status_" + id + ".json");
                Map<String, Object> status = new LinkedHashMap<>();
                status.put("rva", id);
                try {
                    if (Files.exists(statusFile) && Files.readString(statusFile).contains("\"status\": \"ok\"")) {
                        status.put("status", "cached");
                    } else {
                        DecompInterface decompiler = new DecompInterface();
                        try {
                            decompiler.openProgram(currentProgram);
                            DecompileResults result = decompiler.decompileFunction(fn, 90, TaskMonitor.DUMMY);
                            status.put("status", result.decompileCompleted() ? "ok" : "failed");
                            status.put("error", result.getErrorMessage());
                            if (result.decompileCompleted()) {
                                String prefix = "// 功能：Ghidra 原始反编译；业务语义需结合调用索引核对。\n" +
                                    "// 入参和返回：以下原型为 Ghidra 推断，不代表已确认的 C++ 类型。\n" +
                                    "// 地址：victoria3.exe+" + id + "；Ghidra 地址：" + fn.getEntryPoint() + "。\n";
                                List<String> lines = Arrays.asList((prefix + result.getDecompiledFunction().getC()).split("\\R", -1));
                                int parts = (lines.size() + 1799) / 1800;
                                List<String> files = new ArrayList<>();
                                for (int part = 0; part < parts; part++) {
                                    String filename = "function_" + id + (parts > 1 ? "_part" + (part + 1) : "") + ".md";
                                    String header = "# `" + fn.getName() + "`（`victoria3.exe+" + id + "`）\n\n" +
                                        "Ghidra 原始反编译，分片 " + (part + 1) + "/" + parts + "；原始行 " +
                                        (part * 1800 + 1) + "–" + Math.min((part + 1) * 1800, lines.size()) + "。\n\n```cpp\n";
                                    write(codeOutput.resolve(filename), header + String.join("\n", lines.subList(part * 1800,
                                        Math.min((part + 1) * 1800, lines.size()))) + "\n```\n");
                                    files.add(filename);
                                }
                                status.put("files", files); status.put("lines", lines.size());
                            }
                        } finally { decompiler.dispose(); }
                        StringBuilder asm = new StringBuilder();
                        InstructionIterator iterator = currentProgram.getListing().getInstructions(fn.getBody(), true);
                        while (iterator.hasNext()) {
                            Instruction ins = iterator.next();
                            asm.append("+").append(rva(ins.getAddress())).append(" ").append(ins).append("\n");
                        }
                        write(output.resolve("function_" + id + ".asm"), asm.toString());
                        write(statusFile, new GsonBuilder().setPrettyPrinting().create().toJson(status));
                    }
                } catch (Exception e) {
                    status.put("status", "exception"); status.put("error", e.toString());
                    try { write(statusFile, new GsonBuilder().setPrettyPrinting().create().toJson(status)); } catch (Exception ignored) { }
                }
                int count = done.incrementAndGet();
                if (count % 100 == 0) println("EXPORT " + count + "/" + total + " LAST " + id);
            }));
        }
        pool.shutdown();
        for (Future<?> task : tasks) task.get();
        println("EXPORT_DONE " + done.get());
    }

    // 功能：按 PE 异常表恢复占位函数的指令和边界；入参：函数；返回：无，仅修改项目副本。
    private void prepareFunction(Function fn) throws Exception {
        if (fn.isExternal()) return;
        Address entry = fn.getEntryPoint();
        long offset = entry.subtract(imageBase);
        Long end = runtimeRanges.get(offset);
        if (end != null) {
            AddressSet range = new AddressSet(entry, imageBase.add(end - 1));
            new DisassembleCommand(entry, range, true).applyTo(currentProgram, monitor);
            Iterator<Function> overlapping = currentProgram.getFunctionManager().getFunctionsOverlapping(range);
            while (overlapping.hasNext()) {
                Function other = overlapping.next();
                if (!other.equals(fn)) range.delete(other.getBody());
            }
            fn.setBody(range);
        } else if (currentProgram.getListing().getInstructionAt(entry) == null || fn.getBody().getNumAddresses() == 1) {
            FunctionIterator following = currentProgram.getFunctionManager().getFunctions(entry.add(1), true);
            Function next = following.hasNext() ? following.next() : null;
            Address last = entry.add(16383);
            if (next != null && next.getEntryPoint().compareTo(last) < 0) last = next.getEntryPoint().subtract(1);
            Long nextRuntime = runtimeRanges.higherKey(offset);
            if (nextRuntime != null && imageBase.add(nextRuntime - 1).compareTo(last) < 0) last = imageBase.add(nextRuntime - 1);
            new DisassembleCommand(entry, new AddressSet(entry, last), true).applyTo(currentProgram, monitor);
            AddressSetView body = CreateFunctionCmd.getFunctionBody(currentProgram, entry);
            AddressSet safeBody = new AddressSet(body);
            Iterator<Function> all = currentProgram.getFunctionManager().getFunctionsOverlapping(safeBody);
            while (all.hasNext()) {
                Function other = all.next();
                if (!other.equals(fn) && safeBody.intersects(other.getBody())) safeBody.delete(other.getBody());
            }
            fn.setBody(safeBody);
        }
    }

    // 功能：将程序地址转为模块偏移；入参：地址；返回：十六进制 RVA 或外部地址标识。
    private String rva(Address address) {
        if (!address.getAddressSpace().equals(imageBase.getAddressSpace())) return "EXTERNAL_" + address;
        return Long.toHexString(address.subtract(imageBase)).toUpperCase();
    }

    // 功能：以 UTF-8 保存导出文件；入参：路径、内容；返回：无。
    private void write(Path path, String content) throws Exception {
        Files.writeString(path, content, StandardCharsets.UTF_8);
    }
}
