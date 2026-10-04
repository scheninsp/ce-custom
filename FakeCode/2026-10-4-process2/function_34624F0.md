# victoria3.exe+34624F0 完整原始反编译

```cpp
// 功能：Ghidra 完整原始反编译；地址 victoria3.exe+34624F0。
// 入参、返回值：以下原型为 Ghidra 推断，真实 C++ 类型及部分局部变量尚未恢复。
// FUN_1434620e0：victoria3.exe+34620E0。
// FUN_143462470：victoria3.exe+3462470。
// FUN_143462490：victoria3.exe+3462490。
// FUN_1434624f0：victoria3.exe+34624F0。

void FUN_1434624f0(undefined1 *param_1)

{
  char cVar1;
  longlong lVar2;
  undefined1 *puVar3;
  undefined4 local_38;
  undefined1 local_28 [24];
  
  cVar1 = FUN_1434620e0();
  if (cVar1 == '\0') {
    local_38 = 0;
  }
  else {
    local_38 = FUN_143462470();
  }
  puVar3 = local_28;
  for (lVar2 = 0x10; lVar2 != 0; lVar2 = lVar2 + -1) {
    *puVar3 = *param_1;
    param_1 = param_1 + 1;
    puVar3 = puVar3 + 1;
  }
  FUN_143462490(local_28,local_38);
  return;
}


```
