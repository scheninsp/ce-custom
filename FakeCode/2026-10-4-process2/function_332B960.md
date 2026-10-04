# victoria3.exe+332B960 完整原始反编译

```cpp
// 功能：Ghidra 完整原始反编译；地址 victoria3.exe+332B960。
// 入参、返回值：以下原型为 Ghidra 推断，真实 C++ 类型及部分局部变量尚未恢复。
// FUN_1407afbf0：victoria3.exe+7AFBF0。
// FUN_1407e7940：victoria3.exe+7E7940。
// FUN_1433154c0：victoria3.exe+33154C0。
// FUN_143316c50：victoria3.exe+3316C50。
// FUN_143317040：victoria3.exe+3317040。
// FUN_143325770：victoria3.exe+3325770。
// FUN_143327080：victoria3.exe+3327080。
// FUN_14332b960：victoria3.exe+332B960。
// FUN_14332be10：victoria3.exe+332BE10。
// FUN_143331520：victoria3.exe+3331520。
// FUN_143331950：victoria3.exe+3331950。
// FUN_143331d30：victoria3.exe+3331D30。
// FUN_143332d10：victoria3.exe+3332D10。
// FUN_143a92b50：victoria3.exe+3A92B50。
// FUN_144120330：victoria3.exe+4120330。
// FUN_144134db8：victoria3.exe+4134DB8。
// FUN_144137a88：victoria3.exe+4137A88。

/* 警告：部分全局符号在相同地址重叠。 */

undefined8 FUN_14332b960(longlong param_1)

{
  longlong *plVar1;
  int iVar2;
  longlong lVar3;
  longlong *plVar4;
  code *pcVar5;
  bool bVar6;
  char cVar7;
  BOOLEAN BVar8;
  int iVar9;
  undefined8 *puVar10;
  longlong lVar11;
  longlong *plVar12;
  ulonglong uVar13;
  uint uVar14;
  ulonglong uVar15;
  double dVar16;
  undefined8 uVar17;
  ulonglong uVar18;
  undefined8 *local_res8;
  undefined8 *local_res10;
  longlong *local_68;
  undefined8 local_60;
  undefined **local_58;
  
  dVar16 = (double)FUN_143a92b50(DAT_1458e74b8);
  if (DAT_144805b18 < dVar16 - *(double *)(param_1 + 0x400)) {
    if (*(longlong **)(param_1 + 0x3e0) != (longlong *)0x0) {
      (**(code **)(**(longlong **)(param_1 + 0x3e0) + 0x18))();
    }
    uVar17 = FUN_143a92b50(DAT_1458e74b8);
    *(undefined8 *)(param_1 + 0x400) = uVar17;
  }
  AcquireSRWLockExclusive((PSRWLOCK)(*(longlong *)(param_1 + 0x3d8) + 0x98));
  cVar7 = *(char *)(param_1 + 0x290);
  if (cVar7 == '\0') {
    FUN_143331520(*(undefined8 *)(param_1 + 0x3d8),1);
  }
  else if (cVar7 == '\x01') {
    FUN_143331950(*(undefined8 *)(param_1 + 0x3d8),1);
  }
  else if (cVar7 == '\x02') {
    FUN_143331d30(*(undefined8 *)(param_1 + 0x3d8),1);
  }
  FUN_143325770(param_1);
  uVar13 = 0;
  iVar9 = 0;
  local_68 = (longlong *)0x0;
  local_60 = 0;
  lVar3 = *(longlong *)ThreadLocalStoragePointer;
  if ((*(int *)(lVar3 + 0x40) < DAT_145885a00) &&
     (FUN_144134db8(&DAT_145885a00), DAT_145885a00 == -1)) {
    atexit((_func_5014 *)&DAT_14422fb80);
    _Init_thread_footer(&DAT_145885a00);
  }
  local_58 = &PTR_vftable_1450bddc0;
  if (*(int *)(param_1 + 0x2d4) != 0) {
    AcquireSRWLockExclusive((PSRWLOCK)(param_1 + 0x2b8));
    FUN_143332d10(&local_68,param_1 + 0x2c8);
    ReleaseSRWLockExclusive((PSRWLOCK)(param_1 + 0x2b8));
  }
  plVar1 = local_68 + local_60._4_4_;
  uVar15 = _UNK_144805fc8;
  plVar12 = local_68;
  do {
    if (plVar12 == plVar1) {
      if ((*(int *)(lVar3 + 0x40) < DAT_145885a00) &&
         (FUN_144134db8(&DAT_145885a00), DAT_145885a00 == -1)) {
        atexit((_func_5014 *)&DAT_14422fb80);
        _Init_thread_footer(&DAT_145885a00);
      }
      uVar15 = uVar13;
      if (0 < local_60._4_4_) {
        do {
          puVar10 = *(undefined8 **)((longlong)local_68 + uVar15);
          if (puVar10 != (undefined8 *)0x0) {
            (**(code **)*puVar10)(puVar10,0);
            pcVar5 = *(code **)(PTR_vftable_1450bddc0 + 0x10);
            FUN_144137a88(puVar10);
            (*pcVar5)(&PTR_vftable_1450bddc0);
          }
          uVar14 = (int)uVar13 + 1;
          uVar13 = (ulonglong)uVar14;
          uVar15 = uVar15 + 8;
        } while ((int)uVar14 < local_60._4_4_);
      }
      uVar13 = local_60;
      local_60 = local_60 & 0xffffffff;
      if (local_68 != (longlong *)0x0) {
        local_60 = uVar13 & 0xffffffff;
        (**(code **)(*local_58 + 0x10))();
      }
      BVar8 = TryAcquireSRWLockExclusive((PSRWLOCK)(param_1 + 0x2a8));
      if (BVar8 != '\0') {
        iVar9 = FUN_143327080(param_1,1);
        ReleaseSRWLockExclusive((PSRWLOCK)(param_1 + 0x2a8));
      }
      ReleaseSRWLockExclusive((PSRWLOCK)(*(longlong *)(param_1 + 0x3d8) + 0x98));
      FUN_1433154c0(param_1 + 0x418);
      if (iVar9 == 0) {
        local_res8 = (undefined8 *)0x5;
        FUN_1407afbf0(&local_res8);
      }
      return 1;
    }
    plVar4 = (longlong *)*plVar12;
    if (((*(int *)(param_1 + 0x304) == 0) && (*(char *)(param_1 + 0x3f3) != '\0')) ||
       ((*(byte *)(plVar4 + 1) & 6) == 6)) {
      iVar2 = (int)plVar4[2];
      if ((iVar2 == *(int *)(param_1 + 0x3ec)) || (iVar2 == 0)) {
        bVar6 = true;
        if ((iVar2 == 0) && (*(char *)(param_1 + 0x290) == '\x02')) {
          FUN_143316c50(*(undefined8 *)(param_1 + 0x3d8),plVar4);
          bVar6 = true;
        }
      }
      else {
        bVar6 = false;
      }
      if (bVar6) {
        uVar18 = uVar15;
        cVar7 = (**(code **)(param_1 + 0x2a0))(plVar4,0);
        if (cVar7 == '\0') {
          FUN_143317040("Invalid handled command");
        }
        else {
          if (*(char *)(param_1 + 0x348) != '\0') {
            puVar10 = (undefined8 *)(**(code **)(*plVar4 + 0x40))(plVar4,&local_res10);
            local_res8 = (undefined8 *)*puVar10;
            *puVar10 = 0;
            FUN_1407e7940(param_1 + 0x318,&local_res8);
            if (local_res8 != (undefined8 *)0x0) {
              (**(code **)*local_res8)(local_res8,1);
            }
            if (local_res10 != (undefined8 *)0x0) {
              (**(code **)*local_res10)(local_res10,1);
            }
          }
          FUN_14332be10(param_1);
        }
        if (0xf < uVar15) {
          lVar11 = 0;
          if ((0xfff < uVar15 + 1) &&
             (lVar11 = _DAT_fffffffffffffff8, 0x1f < 0xfffffffffffffff8U - _DAT_fffffffffffffff8)) {
                    /* 警告：此调用不返回。 */
            _invoke_watson((wchar_t *)0x0,(wchar_t *)0x0,(wchar_t *)0x0,0,0);
          }
          if (lVar11 != 0) {
            FUN_144120330();
          }
        }
      }
      else {
        FUN_143316c50(*(undefined8 *)(param_1 + 0x3d8),plVar4);
        uVar18 = uVar15;
      }
    }
    else {
      if ((*(int *)(lVar3 + 0x40) < DAT_1458f03e0) &&
         (FUN_144134db8(&DAT_1458f03e0), DAT_1458f03e0 == -1)) {
        atexit((_func_5014 *)&LAB_144237420);
        _Init_thread_footer(&DAT_1458f03e0);
      }
      FUN_143317040("Discarding asynchronous command due to disabled command execution",plVar4);
      uVar18 = uVar15;
    }
    plVar12 = plVar12 + 1;
    uVar15 = uVar18;
  } while( true );
}


```
