from xdsl.dialects.experimental import aie
from xdsl.dialects.builtin import Region, IndexType, ModuleOp, i32, IntegerAttr, ArrayAttr, i64, StringAttr
from xdsl.dialects.arith import Constant
from xdsl.dialects.memref import MemRefType
from xdsl.dialects import builtin, arith, memref
from xdsl.builder import Builder

def I32Attr(value):
    return IntegerAttr.from_int_and_width(value, i32)

def tutorial4():
    col = IntegerAttr.from_int_and_width(1, i32)
    row = IntegerAttr.from_int_and_width(4, i32)
    tile14 = aie.TileOp(col, row)

    col = IntegerAttr.from_int_and_width(3, i32)
    row = IntegerAttr.from_int_and_width(4, i32)
    tile34 = aie.TileOp(col, row)

    elem_number = IntegerAttr.from_int_and_width(1, i32)
    object_fifo = aie.createObjectFifo(elem_number, tile14, tile34, i32, [256], "of")

    lock34_8 = aie.LockOp(I32Attr(8), I32Attr(0), tile34, StringAttr("lock_a34_8"))

    arith.Constant.from_int_and_width
    acquire_fifo = aie.ObjectFifoAcquireOp(I32Attr(0), I32Attr(1), object_fifo.sym_name)

    @Builder.region
    def core14_region(builder: Builder):
        builder.insert(acquire_fifo)

    stackSize = IntegerAttr.from_int_and_width(1, i32)
    core14 = aie.CoreOp(stackSize, tile14, core14_region)

    @Builder.region
    def region0(builder: Builder):
        builder.insert(tile14)
        builder.insert(tile34)
        builder.insert(object_fifo)
        builder.insert(lock34_8)
        builder.insert(core14)

    device_val = IntegerAttr.from_int_and_width(0, i32)
    device = aie.DeviceOp(device_val, region0)

    module = builtin.ModuleOp([device])
    print(module)

if __name__ == "__main__":
    tutorial4()
