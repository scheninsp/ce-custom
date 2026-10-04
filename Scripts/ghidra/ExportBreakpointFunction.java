// 功能：按 PE 异常目录边界导出断点所属函数及指定辅助函数，不保存 Ghidra 项目修改。
// 入参：输出目录和一个或多个十六进制 RVA；返回：元数据、完整指令和原始反编译文件。
// @category Victoria3
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.MemoryBlock;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import com.google.gson.GsonBuilder;

public class ExportBreakpointFunction extends GhidraScript {
    // 功能：定位、补齐指令并导出函数；入参来自脚本参数；返回：无。
    @Override public void run() throws Exception {
        String[] args = getScriptArgs();
        Path output = Paths.get(args[0]);
        Files.createDirectories(output);
        Address base = currentProgram.getImageBase();
        MemoryBlock pdata = currentProgram.getMemory().getBlock(".pdata");
        DecompInterface decompiler = new DecompInterface();
        decompiler.openProgram(currentProgram);
        try {
            for (int a = 1; a < args.length; a++) {
                long target = Long.parseLong(args[a], 16), begin = -1, end = -1;
                for (long offset = 0; offset + 12 <= pdata.getSize(); offset += 12) {
                    long b = Integer.toUnsignedLong(currentProgram.getMemory().getInt(pdata.getStart().add(offset)));
                    long e = Integer.toUnsignedLong(currentProgram.getMemory().getInt(pdata.getStart().add(offset + 4)));
                    if (b <= target && target < e) { begin = b; end = e; break; }
                }
                if (begin < 0) {
                    Function leaf = currentProgram.getFunctionManager().getFunctionContaining(base.add(target));
                    if (leaf == null) leaf = createFunction(base.add(target), null);
                    if (leaf == null) throw new IllegalStateException("No function for " + args[a]);
                    begin = leaf.getEntryPoint().subtract(base);
                    end = leaf.getBody().getMaxAddress().subtract(base) + 1;
                }
                Address start = base.add(begin), last = base.add(end - 1);
                AddressSet range = new AddressSet(start, last);
                new DisassembleCommand(start, range, true).applyTo(currentProgram, monitor);
                Function fn = currentProgram.getFunctionManager().getFunctionAt(start);
                if (fn == null) {
                    new CreateFunctionCmd(start).applyTo(currentProgram, monitor);
                    fn = currentProgram.getFunctionManager().getFunctionAt(start);
                }
                if (fn == null) throw new IllegalStateException("Function creation failed");
                fn.setBody(range);
                decompiler.flushCache();
                DecompileResults result = decompiler.decompileFunction(fn, 120, monitor);
                String id = Long.toHexString(begin).toUpperCase();
                Map<String,Object> meta = new LinkedHashMap<>();
                meta.put("target_rva", args[a]); meta.put("begin_rva", id);
                meta.put("end_rva_exclusive", Long.toHexString(end).toUpperCase());
                meta.put("name", fn.getName()); meta.put("program", currentProgram.getName());
                meta.put("executable_path", currentProgram.getExecutablePath());
                meta.put("sha256", currentProgram.getExecutableSHA256());
                meta.put("decompile_completed", result.decompileCompleted());
                meta.put("error", result.getErrorMessage());
                byte[] all = new byte[(int)(end-begin)];
                currentProgram.getMemory().getBytes(start, all);
                StringBuilder hex = new StringBuilder();
                for (byte b : all) hex.append(String.format("%02X", b & 255));
                meta.put("bytes", hex.toString());
                StringBuilder asm = new StringBuilder("RVA\tBytes\tInstruction\n");
                int count = 0, length = 0;
                InstructionIterator instructions = currentProgram.getListing().getInstructions(range, true);
                while (instructions.hasNext()) {
                    Instruction ins = instructions.next();
                    StringBuilder bytes = new StringBuilder();
                    for (byte b : ins.getBytes()) bytes.append(String.format("%02X", b & 255));
                    asm.append(Long.toHexString(ins.getAddress().subtract(base)).toUpperCase())
                        .append('\t').append(bytes).append('\t').append(ins.toString()).append('\n');
                    count++; length += ins.getLength();
                }
                meta.put("instruction_count", count); meta.put("decoded_bytes", length);
                Files.writeString(output.resolve("function_"+id+".json"), new GsonBuilder().setPrettyPrinting().create().toJson(meta), StandardCharsets.UTF_8);
                Files.writeString(output.resolve("function_"+id+".tsv"), asm, StandardCharsets.UTF_8);
                if (!result.decompileCompleted()) throw new IllegalStateException(result.getErrorMessage());
                Files.writeString(output.resolve("function_"+id+".c"), result.getDecompiledFunction().getC(), StandardCharsets.UTF_8);
                println("EXPORTED " + id + " END " + Long.toHexString(end) + " INSTRUCTIONS " + count);
            }
        } finally { decompiler.dispose(); }
    }
}
