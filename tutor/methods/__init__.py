"""Method step definitions and assembly for the Tutor Framework."""

from tutor.framework import SolveMethod
from tutor.methods.cfop import WhiteCrossStep as CFOPCross, F2LPairStep, OLLStep, PLLStep
from tutor.methods.beginner import (
    DaisyStep,
    WhiteCrossStep as BeginnerCross,
    FirstLayerCornerStep,
    SecondLayerEdgeStep,
    YellowCrossStep,
    YellowFaceStep,
    PLLStep as BeginnerPLL
)

def get_cfop_method() -> SolveMethod:
    """Returns the instantiated CFOP Method sequence."""
    steps = [
        CFOPCross(),
        F2LPairStep(1),
        F2LPairStep(2),
        F2LPairStep(3),
        F2LPairStep(4),
        OLLStep(),
        PLLStep(),
    ]
    return SolveMethod("CFOP", steps)

def get_beginner_method() -> SolveMethod:
    """Returns the instantiated Beginner Method sequence."""
    steps = [
        DaisyStep(),
        BeginnerCross(),
        FirstLayerCornerStep(1),
        FirstLayerCornerStep(2),
        FirstLayerCornerStep(3),
        FirstLayerCornerStep(4),
        SecondLayerEdgeStep(1),
        SecondLayerEdgeStep(2),
        SecondLayerEdgeStep(3),
        SecondLayerEdgeStep(4),
        YellowCrossStep(),
        YellowFaceStep(),
        BeginnerPLL(),
    ]
    return SolveMethod("Beginner's Method", steps)

def get_roux_method() -> SolveMethod:
    from tutor.methods.roux import FirstBlockStep, SecondBlockStep, CMLLStep, LSEStep
    steps = [
        FirstBlockStep(),
        SecondBlockStep(),
        CMLLStep(),
        LSEStep(),
    ]
    return SolveMethod("Roux", steps)

def get_zz_method() -> SolveMethod:
    from tutor.methods.zz import EOLineStep, ZZF2LStep, LLStep
    steps = [
        EOLineStep(),
        ZZF2LStep(),
        LLStep(),
    ]
    return SolveMethod("ZZ", steps)
