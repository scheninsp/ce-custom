# victoria3.exe+3327080 完整原始反编译

```cpp
// 功能：Ghidra 完整原始反编译；地址 victoria3.exe+3327080。
// 入参、返回值：以下原型为 Ghidra 推断，真实 C++ 类型及部分局部变量尚未恢复。
// FUN_1406157e0：victoria3.exe+6157E0。
// FUN_1406174c0：victoria3.exe+6174C0。
// FUN_1406372f0：victoria3.exe+6372F0。
// FUN_1407e7940：victoria3.exe+7E7940。
// FUN_140be6920：victoria3.exe+BE6920。
// FUN_142aa77b0：victoria3.exe+2AA77B0。
// FUN_143290260：victoria3.exe+3290260。
// FUN_143316c50：victoria3.exe+3316C50。
// FUN_143317040：victoria3.exe+3317040。
// FUN_143326a30：victoria3.exe+3326A30。
// FUN_143326e10：victoria3.exe+3326E10。
// FUN_143327080：victoria3.exe+3327080。
// FUN_143332d10：victoria3.exe+3332D10。
// FUN_1434624f0：victoria3.exe+34624F0。
// FUN_143af0cd0：victoria3.exe+3AF0CD0。
// FUN_143b01fd0：victoria3.exe+3B01FD0。
// FUN_14410ff70：victoria3.exe+410FF70。
// FUN_144120330：victoria3.exe+4120330。
// FUN_14412d1c8：victoria3.exe+412D1C8。
// FUN_144134db8：victoria3.exe+4134DB8。
// FUN_14417d4c0：victoria3.exe+417D4C0。

int FUN_143327080(longlong *param_1,char param_2)

{
  PSRWLOCK pRVar1;
  int iVar2;
  undefined8 uVar3;
  undefined1 auVar4 [16];
  bool bVar5;
  bool bVar6;
  bool bVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  longlong *plVar11;
  bool bVar12;
  char cVar13;
  uint uVar14;
  undefined4 uVar15;
  undefined8 *puVar16;
  longlong lVar17;
  uint uVar18;
  uint uVar19;
  int iVar20;
  ulonglong uVar21;
  longlong *plVar22;
  longlong lVar23;
  longlong *plVar24;
  ulonglong uVar25;
  longlong *plVar26;
  longlong *plVar27;
  longlong lVar28;
  undefined8 uVar29;
  undefined8 uVar30;
  undefined4 uVar31;
  float fVar32;
  int local_res18;
  longlong *local_res20;
  undefined8 local_1f8;
  uint uStack_1f0;
  undefined4 uStack_1ec;
  undefined1 local_1e8 [16];
  longlong local_1d8;
  ulonglong local_1d0;
  undefined4 *local_1c8;
  undefined1 *puStack_1c0;
  undefined8 local_1b8;
  undefined4 uStack_1b0;
  undefined4 uStack_1ac;
  undefined8 local_1a8;
  code *local_1a0;
  longlong *local_198;
  longlong *local_188;
  uint5 uStack_180;
  undefined3 uStack_17b;
  longlong *local_178;
  undefined8 *puStack_170;
  longlong *local_168;
  undefined8 local_160;
  undefined **local_158;
  undefined4 local_148;
  undefined4 uStack_144;
  uint uStack_140;
  uint uStack_13c;
  undefined8 local_138;
  code *pcStack_130;
  undefined1 *local_128;
  code *local_120;
  int local_118;
  longlong *local_110;
  undefined8 *local_108;
  longlong local_100;
  undefined1 *local_f8;
  uint uStack_f0;
  uint uStack_ec;
  undefined8 local_e8;
  undefined8 *local_e0;
  char *local_d8;
  undefined8 local_d0;
  PSRWLOCK local_c8;
  undefined1 local_c0;
  PSRWLOCK local_b8;
  undefined1 local_b0;
  undefined8 local_a8;
  undefined4 *local_a0;
  char *local_98;
  undefined8 local_90;
  
  plVar27 = (longlong *)0x0;
  local_res18 = 0;
  fVar32 = DAT_144805b28;
  if (*(char *)((longlong)param_1 + 0x3f2) != '\0') {
    local_168 = (longlong *)0x0;
    local_160 = (undefined4 *)0x0;
    iVar20 = 0;
    if ((*(int *)(*(longlong *)ThreadLocalStoragePointer + 0x40) < DAT_145885a00) &&
       (FUN_144134db8(&DAT_145885a00), DAT_145885a00 == -1)) {
      atexit((_func_5014 *)&DAT_14422fb80);
      _Init_thread_footer(&DAT_145885a00);
    }
    local_158 = &PTR_vftable_1450bddc0;
    AcquireSRWLockExclusive((PSRWLOCK)(param_1 + 0x81));
    plVar26 = (longlong *)param_1[0x5c];
    local_198 = plVar26 + *(int *)((longlong)param_1 + 0x2ec);
    plVar22 = plVar27;
    plVar11 = local_168;
    if (plVar26 != local_198) {
      do {
        lVar28 = *plVar26;
        if (iVar20 == (int)plVar27) {
          uVar18 = (uint)((float)(int)plVar27 * fVar32);
          uVar14 = iVar20 + 1U;
          if ((int)(iVar20 + 1U) < (int)uVar18) {
            uVar14 = uVar18;
          }
          plVar27 = (longlong *)(ulonglong)uVar14;
          local_res20 = (longlong *)
                        (**(code **)(PTR_vftable_1450bddc0 + 8))
                                  (&PTR_vftable_1450bddc0,(ulonglong)uVar14 << 3,8);
          local_res20[iVar20] = lVar28;
          plVar11 = local_res20;
          for (plVar24 = plVar22; plVar24 != plVar22 + iVar20; plVar24 = plVar24 + 1) {
            lVar28 = *plVar24;
            *plVar24 = 0;
            *plVar11 = lVar28;
            puVar16 = (undefined8 *)*plVar24;
            if (puVar16 != (undefined8 *)0x0) {
              (**(code **)*puVar16)(puVar16,1);
            }
            plVar11 = plVar11 + 1;
          }
          (**(code **)(PTR_vftable_1450bddc0 + 0x10))(&PTR_vftable_1450bddc0,plVar22);
          local_160 = (undefined4 *)(ulonglong)uVar14;
          plVar22 = local_res20;
        }
        else {
          plVar22[iVar20] = lVar28;
        }
        iVar20 = iVar20 + 1;
        local_160 = (undefined4 *)CONCAT44(iVar20,(undefined4)local_160);
        plVar26 = plVar26 + 1;
        plVar11 = plVar22;
      } while (plVar26 != local_198);
    }
    local_168 = plVar11;
    uVar25 = 0;
    *(undefined4 *)((longlong)param_1 + 0x2ec) = 0;
    ReleaseSRWLockExclusive((PSRWLOCK)(param_1 + 0x81));
    local_178 = (longlong *)0x1;
    puStack_170 = &local_1f8;
    local_188 = (longlong *)0x14476db48;
    _uStack_180 = 0x1f;
    local_1f8._0_4_ = iVar20;
    FUN_14410ff70(local_1e8,&local_188,&local_178);
    local_1c8 = (undefined4 *)local_1e8;
    if (0xf < local_1d0) {
      local_1c8 = (undefined4 *)local_1e8._0_8_;
    }
    puStack_1c0._0_5_ = (uint5)(uint)local_1d8;
    local_1f8._0_4_ = (int)local_1c8;
    local_1f8._4_4_ = (undefined4)((ulonglong)local_1c8 >> 0x20);
    uStack_1f0 = (uint)local_1d8;
    uStack_1ec = (undefined4)((ulonglong)puStack_1c0 >> 0x20);
    FUN_143b01fd0("C:\\mnt\\gsg\\caligula\\caligula\\cw\\jomini\\modules\\session\\source\\session.cpp"
                  ,0x516,0x10003,2,&local_1f8);
    if (0xf < local_1d0) {
      lVar28 = local_1e8._0_8_;
      if ((0xfff < local_1d0 + 1) &&
         (lVar28 = *(longlong *)(local_1e8._0_8_ + -8), 0x1f < (local_1e8._0_8_ - lVar28) - 8U)) {
                    /* 警告：此调用不返回。 */
        _invoke_watson((wchar_t *)0x0,(wchar_t *)0x0,(wchar_t *)0x0,0,0);
      }
      if (lVar28 != 0) {
        FUN_144120330(lVar28);
      }
    }
    FUN_143326e10(param_1,&local_168);
    lVar28 = (longlong)local_160._4_4_;
    local_res18 = local_160._4_4_;
    *(undefined1 *)((longlong)param_1 + 0x3f2) = 0;
    FUN_142aa77b0(param_1,0);
    local_178 = (longlong *)0x0;
    puStack_170 = &local_1f8;
    local_188 = (longlong *)0x14476da90;
    _uStack_180 = 0x2e;
    FUN_14410ff70(local_1e8,&local_188,&local_178);
    local_1c8 = (undefined4 *)local_1e8;
    if (0xf < local_1d0) {
      local_1c8 = (undefined4 *)local_1e8._0_8_;
    }
    puStack_1c0._0_5_ = (uint5)(uint)local_1d8;
    local_1f8._0_4_ = (int)local_1c8;
    local_1f8._4_4_ = (undefined4)((ulonglong)local_1c8 >> 0x20);
    uStack_1f0 = (uint)local_1d8;
    uStack_1ec = (undefined4)((ulonglong)puStack_1c0 >> 0x20);
    FUN_143b01fd0("C:\\mnt\\gsg\\caligula\\caligula\\cw\\jomini\\modules\\session\\source\\session.cpp"
                  ,0x51d,0x10003,2,&local_1f8);
    if (0xf < local_1d0) {
      lVar23 = local_1e8._0_8_;
      if ((0xfff < local_1d0 + 1) &&
         (lVar23 = *(longlong *)(local_1e8._0_8_ + -8), 0x1f < (local_1e8._0_8_ - lVar23) - 8U)) {
                    /* 警告：此调用不返回。 */
        _invoke_watson((wchar_t *)0x0,(wchar_t *)0x0,(wchar_t *)0x0,0,0);
      }
      if (lVar23 != 0) {
        FUN_144120330(lVar23);
      }
    }
    *(undefined4 *)(param_1 + 3) = 0;
    *(int *)((longlong)param_1 + 0x1c) = *(int *)((longlong)param_1 + 0xc);
    uVar21 = uVar25;
    if (0 < *(int *)((longlong)param_1 + 0xc)) {
      do {
        local_res20 = (longlong *)CONCAT44(local_res20._4_4_,4);
        plVar27 = *(longlong **)(*param_1 + 0x40 + (longlong)(int)uVar21 * 0x48);
        if (plVar27 == (longlong *)0x0) {
                    /* 警告：此调用不返回。 */
          FUN_14412d1c8();
        }
        (**(code **)(*plVar27 + 0x10))(plVar27,&local_res20);
        *(int *)(param_1 + 3) = (int)param_1[3] + 1;
        uVar21 = (ulonglong)*(uint *)(param_1 + 3);
      } while ((int)*(uint *)(param_1 + 3) < *(int *)((longlong)param_1 + 0x1c));
    }
    plVar27 = local_168;
    param_1[3] = 0;
    if (local_168 != (longlong *)0x0) {
      if (0 < lVar28) {
        do {
          puVar16 = (undefined8 *)plVar27[uVar25];
          if (puVar16 != (undefined8 *)0x0) {
            (**(code **)*puVar16)(puVar16,1);
          }
          uVar25 = uVar25 + 1;
        } while ((longlong)uVar25 < lVar28);
      }
      (**(code **)(*local_158 + 0x10))(local_158,plVar27);
    }
  }
  iVar20 = 0;
  if ((*(char *)((longlong)param_1 + 0x3f3) == '\0') || (*(int *)((longlong)param_1 + 0x304) == 0))
  {
    bVar6 = false;
    bVar7 = false;
  }
  else {
    bVar6 = true;
    bVar7 = true;
    FUN_143326e10(param_1,param_1 + 0x5f);
    local_res18 = local_res18 + *(int *)((longlong)param_1 + 0x304);
    FUN_140be6920(param_1 + 0x5f);
  }
  *(undefined1 *)((longlong)param_1 + 0x3f7) = 1;
  lVar28 = param_1[0x7b];
  pRVar1 = (PSRWLOCK)(lVar28 + 0x88);
  local_1f8 = pRVar1;
  AcquireSRWLockExclusive(pRVar1);
  uStack_1f0 = CONCAT31(uStack_1f0._1_3_,1);
  plVar27 = (longlong *)(lVar28 + 0x48);
  local_110 = plVar27;
  FUN_143332d10(plVar27,lVar28 + 0x60);
  ReleaseSRWLockExclusive(pRVar1);
  *(bool *)((longlong)param_1 + 0x3f7) = *(int *)(lVar28 + 0x54) != 0;
  pRVar1 = local_1f8;
  if (param_2 == '\0') {
    AcquireSRWLockExclusive((PSRWLOCK)(param_1[0x7b] + 0x98));
    pRVar1 = local_1f8;
  }
  local_1f8._4_4_ = (undefined4)((ulonglong)pRVar1 >> 0x20);
  local_res20 = (longlong *)((ulonglong)local_res20 & 0xffffffff00000000);
  iVar2 = *(int *)(lVar28 + 0x54);
  if (0 < iVar2) {
    local_198 = (longlong *)0x0;
    local_118 = iVar2 + -1;
    uVar30 = CONCAT44(uStack_1f0,local_1f8._4_4_);
    uVar29 = CONCAT44(uStack_1f0,local_1f8._4_4_);
    local_100 = (longlong)iVar2;
    uVar31 = local_1f8._4_4_;
    uVar14 = uStack_1f0;
    do {
      plVar26 = local_198;
      plVar27 = *(longlong **)(*plVar27 + (longlong)local_198 * 8);
      iVar2 = (int)plVar27[2];
      if ((iVar2 == *(int *)((longlong)param_1 + 0x3ec)) || (iVar2 == 0)) {
        bVar5 = true;
        bVar12 = true;
        if ((*(char *)((longlong)param_1 + 0x3f1) == '\0') || ((*(byte *)(plVar27 + 1) & 2) != 0))
        goto LAB_1433275e2;
        bVar12 = true;
      }
      else {
        bVar12 = false;
LAB_1433275e2:
        bVar5 = bVar12;
        bVar12 = false;
      }
      *(bool *)((longlong)param_1 + 0x3f7) = iVar20 != local_118;
      local_1f8 = pRVar1;
      if (((*(byte *)(plVar27 + 1) & 6) == 6) && ((*(byte *)(plVar27 + 1) & 2) == 0)) {
        uVar15 = (**(code **)(*plVar27 + 0x48))(plVar27);
        local_1a8 = FUN_143af0cd0(uVar15);
        uStack_1b0 = uVar14;
        local_1b8._0_4_ = *(undefined4 *)((longlong)plVar27 + 0x14);
        uStack_1ac = uStack_1ec;
        local_1a0 = FUN_1406372f0;
        local_e8 = 0xf2;
        local_e0 = &local_1b8;
        local_d8 = 
        "Command is marked AlwaysExecute | Recordable - this is a bug and means the command may be executed twice! id: {}, type: {}"
        ;
        local_d0 = 0x7a;
        local_1b8._4_4_ = uVar31;
        uVar14 = uStack_1b0;
        FUN_14410ff70(local_1e8,&local_d8,&local_e8);
        local_f8 = local_1e8;
        if (0xf < local_1d0) {
          local_f8 = (undefined1 *)local_1e8._0_8_;
        }
        uStack_f0 = (uint)local_1d8;
        uStack_ec = uStack_ec & 0xffffff00;
        local_148 = SUB84(local_f8,0);
        uStack_144 = (undefined4)((ulonglong)local_f8 >> 0x20);
        uStack_140 = (uint)local_1d8;
        uStack_13c = uStack_ec;
        FUN_143b01fd0("C:\\mnt\\gsg\\caligula\\caligula\\cw\\jomini\\modules\\session\\source\\session.cpp"
                      ,0x540,3,4,&local_148);
        local_1b8 = (longlong *)CONCAT44(local_1b8._4_4_,(undefined4)local_1b8);
        if (0xf < local_1d0) {
          lVar28 = local_1e8._0_8_;
          if ((0xfff < local_1d0 + 1) &&
             (lVar28 = *(longlong *)(local_1e8._0_8_ + -8), 0x1f < (local_1e8._0_8_ - lVar28) - 8U))
          {
                    /* 警告：此调用不返回。 */
            _invoke_watson((wchar_t *)0x0,(wchar_t *)0x0,(wchar_t *)0x0,0,0);
          }
          local_1b8 = (longlong *)CONCAT44(local_1b8._4_4_,(undefined4)local_1b8);
          if (lVar28 != 0) {
            FUN_144120330();
          }
        }
      }
      if (((bVar6) || (*(char *)((longlong)param_1 + 0x3f3) == '\0')) &&
         ((*(byte *)(plVar27 + 1) & 6) != 6)) {
        if (bVar12) {
LAB_143327bcd:
          if (*(int *)(*(longlong *)ThreadLocalStoragePointer + 0x40) < DAT_1458f03e0) {
            FUN_144134db8(&DAT_1458f03e0);
            if (DAT_1458f03e0 == -1) {
              atexit((_func_5014 *)&LAB_144237420);
              _Init_thread_footer(&DAT_1458f03e0);
            }
          }
          FUN_143317040("Recording command.",plVar27);
          plVar22 = param_1 + 0x5c;
          iVar20 = *(int *)((longlong)param_1 + 0x2ec);
          if (iVar20 == (int)param_1[0x5d]) {
            uVar19 = (uint)((float)(int)param_1[0x5d] * fVar32);
            uVar18 = iVar20 + 1U;
            if ((int)(iVar20 + 1U) < (int)uVar19) {
              uVar18 = uVar19;
            }
            lVar17 = (**(code **)(*(longlong *)param_1[0x5e] + 8))
                               ((longlong *)param_1[0x5e],(ulonglong)uVar18 << 3,8);
            *(longlong **)(lVar17 + (longlong)*(int *)((longlong)param_1 + 0x2ec) * 8) = plVar27;
            lVar23 = *plVar22;
            lVar28 = (longlong)*(int *)((longlong)param_1 + 0x2ec) * 8;
            if (lVar23 != lVar23 + lVar28) {
              FUN_14417d4c0(lVar17,lVar23,lVar28);
            }
            iVar20 = *(int *)((longlong)param_1 + 0x2ec);
            *(undefined4 *)((longlong)param_1 + 0x2ec) = 0;
            FUN_1406174c0(plVar22,lVar17);
            *(int *)((longlong)param_1 + 0x2ec) = iVar20 + 1;
            *(undefined8 *)(*local_110 + (longlong)local_198 * 8) = 0;
            plVar26 = local_198;
            pRVar1 = local_1f8;
          }
          else {
            *(longlong **)(*plVar22 + (longlong)iVar20 * 8) = plVar27;
            *(int *)((longlong)param_1 + 0x2ec) = *(int *)((longlong)param_1 + 0x2ec) + 1;
            *(undefined8 *)(*local_110 + (longlong)plVar26 * 8) = 0;
            pRVar1 = local_1f8;
          }
        }
        else {
          if (*(int *)(*(longlong *)ThreadLocalStoragePointer + 0x40) < DAT_1458f03e0) {
            FUN_144134db8(&DAT_1458f03e0);
            if (DAT_1458f03e0 == -1) {
              atexit((_func_5014 *)&LAB_144237420);
              _Init_thread_footer(&DAT_1458f03e0);
            }
          }
          FUN_143317040("Discarding command.",plVar27);
          pRVar1 = local_1f8;
        }
      }
      else {
        local_1d8 = 0;
        local_1d0 = 0xf;
        local_1e8._1_15_ = SUB1615((undefined1  [16])0x0,1);
        auVar4[0xf] = 0;
        auVar4._0_15_ = local_1e8._1_15_;
        local_1e8 = auVar4 << 8;
        cVar13 = (*(code *)param_1[0x54])(plVar27,0);
        if (cVar13 == '\0') {
          FUN_143317040("Invalid command.",plVar27,local_1e8);
          FUN_143326a30(&local_1b8,plVar27);
          FUN_143317040("Command data:",plVar27);
          FUN_1406157e0(&local_1b8);
          if ((iVar2 != 0) && (bVar5)) {
            if (local_1d8 == 0) {
              uVar15 = (**(code **)(*plVar27 + 0x48))();
              local_138 = FUN_143af0cd0(uVar15);
              local_148 = *(undefined4 *)((longlong)plVar27 + 0x14);
              uStack_144 = (undefined4)uVar29;
              uStack_140 = (uint)((ulonglong)uVar29 >> 0x20);
              uStack_13c = uStack_1ec;
              pcStack_130 = FUN_1406372f0;
              local_a8 = 0xf2;
              local_a0 = &local_148;
              local_98 = "Out of sync! Invalid command. ID: {} Type: {}";
              local_90 = 0x2d;
              FUN_14410ff70(&local_1b8,&local_98,&local_a8);
              local_188 = &local_1b8;
              if ((code *)0xf < local_1a0) {
                local_188 = local_1b8;
              }
              uStack_180 = (uint5)(uint)local_1a8;
              local_148 = SUB84(local_188,0);
              uStack_144 = (undefined4)((ulonglong)local_188 >> 0x20);
              uStack_140 = (uint)local_1a8;
              uStack_13c = (uint)((ulonglong)_uStack_180 >> 0x20);
              FUN_143b01fd0("C:\\mnt\\gsg\\caligula\\caligula\\cw\\jomini\\modules\\session\\source\\session.cpp"
                            ,0x569,3,4,&local_148);
              if ((code *)0xf < local_1a0) {
                plVar22 = local_1b8;
                if (((code *)0xfff < local_1a0 + 1) &&
                   (plVar22 = (longlong *)local_1b8[-1],
                   0x1f < (ulonglong)((longlong)local_1b8 + (-8 - (longlong)plVar22)))) {
                    /* 警告：此调用不返回。 */
                  _invoke_watson((wchar_t *)0x0,(wchar_t *)0x0,(wchar_t *)0x0,0,0);
                }
LAB_143327b7c:
                if (plVar22 != (longlong *)0x0) {
                  FUN_144120330();
                }
              }
            }
            else {
              uVar15 = (**(code **)(*plVar27 + 0x48))(plVar27);
              local_138 = FUN_143af0cd0(uVar15);
              local_148 = *(undefined4 *)((longlong)plVar27 + 0x14);
              uStack_144 = (undefined4)uVar30;
              uStack_140 = (uint)((ulonglong)uVar30 >> 0x20);
              uStack_13c = uStack_1ec;
              pcStack_130 = FUN_1406372f0;
              local_128 = local_1e8;
              local_120 = FUN_1406372f0;
              local_168 = (longlong *)0xff2;
              local_160 = &local_148;
              local_1f8._0_4_ = 0x4476d968;
              local_1f8._4_4_ = 1;
              uStack_1f0 = 0x30;
              uStack_1ec = 0;
              FUN_14410ff70(&local_1b8,&local_1f8,&local_168);
              local_178 = &local_1b8;
              if ((code *)0xf < local_1a0) {
                local_178 = local_1b8;
              }
              puStack_170._0_5_ = (uint5)(uint)local_1a8;
              local_148 = SUB84(local_178,0);
              uStack_144 = (undefined4)((ulonglong)local_178 >> 0x20);
              uStack_140 = (uint)local_1a8;
              uStack_13c = (uint)((ulonglong)puStack_170 >> 0x20);
              FUN_143b01fd0("C:\\mnt\\gsg\\caligula\\caligula\\cw\\jomini\\modules\\session\\source\\session.cpp"
                            ,0x56d,3,4,&local_148);
              if ((code *)0xf < local_1a0) {
                plVar22 = local_1b8;
                if (((code *)0xfff < local_1a0 + 1) &&
                   (plVar22 = (longlong *)local_1b8[-1],
                   0x1f < (ulonglong)((longlong)local_1b8 + (-8 - (longlong)plVar22)))) {
                    /* 警告：此调用不返回。 */
                  _invoke_watson((wchar_t *)0x0,(wchar_t *)0x0,(wchar_t *)0x0,0,0);
                }
                goto LAB_143327b7c;
              }
            }
          }
        }
        else {
          if ((iVar2 == 0) && ((char)param_1[0x52] == '\x02')) {
            pRVar1 = (PSRWLOCK)param_1[0x7a];
            local_c8 = pRVar1;
            AcquireSRWLockExclusive(pRVar1);
            local_c0 = 1;
            FUN_143316c50(param_1[0x7b],plVar27);
            ReleaseSRWLockExclusive(pRVar1);
            local_c0 = 0;
          }
          if (bVar5) {
            if ((char)param_1[0x69] != '\0') {
              puVar16 = (undefined8 *)(**(code **)(*plVar27 + 0x40))(plVar27,&local_108);
              uVar3 = *puVar16;
              *puVar16 = 0;
              local_148 = (undefined4)uVar3;
              uStack_144 = (undefined4)((ulonglong)uVar3 >> 0x20);
              FUN_1407e7940(param_1 + 99,&local_148);
              puVar16 = (undefined8 *)CONCAT44(uStack_144,local_148);
              if (puVar16 != (undefined8 *)0x0) {
                (**(code **)*puVar16)(puVar16,1);
              }
              if (local_108 != (undefined8 *)0x0) {
                (**(code **)*local_108)(local_108,1);
              }
            }
            uVar9 = uStack_144;
            uVar15 = local_148;
            plVar26 = param_1 + 0x90;
            lVar28 = *plVar26;
            uStack_1b0 = (undefined4)lVar28;
            uStack_1ac = (undefined4)((ulonglong)lVar28 >> 0x20);
            *plVar26 = (longlong)plVar27;
            local_1a8 = CONCAT71(local_1a8._1_7_,1);
            lVar23 = *(longlong *)ThreadLocalStoragePointer;
            if ((*(byte *)(plVar27 + 1) & 1) == 0) {
              *(undefined4 *)(lVar23 + 0x92c) = 1;
            }
            plVar22 = (longlong *)param_1[0x7c];
            local_148 = SUB84(plVar27,0);
            uVar8 = local_148;
            uStack_144 = (undefined4)((ulonglong)plVar27 >> 0x20);
            uVar10 = uStack_144;
            local_1b8 = plVar26;
            if (plVar22 == (longlong *)0x0) {
              local_1c8 = &local_148;
              puStack_1c0 = &LAB_143334170;
              FUN_1434624f0(&local_1c8);
            }
            else {
              local_148 = uVar15;
              uStack_144 = uVar9;
              cVar13 = (**(code **)(*plVar22 + 0x38))(plVar22,0);
              local_1c8 = &local_148;
              puStack_1c0 = &LAB_143334170;
              local_148 = uVar8;
              uStack_144 = uVar10;
              FUN_1434624f0(&local_1c8);
              if ((cVar13 != '\0') &&
                 (plVar22 = (longlong *)param_1[0x7c], plVar22 != (longlong *)0x0)) {
                (**(code **)(*plVar22 + 0x38))(plVar22,1);
              }
            }
            *(undefined4 *)(lVar23 + 0x92c) = 0;
            *plVar26 = lVar28;
            plVar26 = local_198;
          }
          else {
            pRVar1 = (PSRWLOCK)param_1[0x7a];
            local_b8 = pRVar1;
            AcquireSRWLockExclusive(pRVar1);
            local_b0 = 1;
            FUN_143316c50(param_1[0x7b],plVar27);
            ReleaseSRWLockExclusive(pRVar1);
            local_b0 = 0;
          }
        }
        if (0xf < local_1d0) {
          lVar28 = local_1e8._0_8_;
          if ((0xfff < local_1d0 + 1) &&
             (lVar28 = *(longlong *)(local_1e8._0_8_ + -8), 0x1f < (local_1e8._0_8_ - lVar28) - 8U))
          {
                    /* 警告：此调用不返回。 */
            _invoke_watson((wchar_t *)0x0,(wchar_t *)0x0,(wchar_t *)0x0,0,0);
          }
          if (lVar28 != 0) {
            FUN_144120330();
          }
        }
        pRVar1 = local_1f8;
        if (bVar12) goto LAB_143327bcd;
      }
      iVar20 = (int)local_res20 + 1;
      local_res20 = (longlong *)CONCAT44(local_res20._4_4_,iVar20);
      local_198 = (longlong *)((longlong)plVar26 + 1);
      plVar27 = local_110;
      bVar6 = bVar7;
    } while ((longlong)local_198 < local_100);
  }
  iVar20 = *(int *)((longlong)plVar27 + 0xc);
  local_1f8 = pRVar1;
  if (*(int *)(*(longlong *)ThreadLocalStoragePointer + 0x40) < DAT_145885a00) {
    FUN_144134db8(&DAT_145885a00);
    if (DAT_145885a00 == -1) {
      atexit((_func_5014 *)&DAT_14422fb80);
      _Init_thread_footer(&DAT_145885a00);
    }
  }
  FUN_143290260(plVar27,&PTR_vftable_1450bddc0);
  if (param_2 == '\0') {
    ReleaseSRWLockExclusive((PSRWLOCK)(param_1[0x7b] + 0x98));
  }
  return local_res18 + iVar20;
}


```
