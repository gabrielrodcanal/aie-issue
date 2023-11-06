from xdsl.dialects.experimental import aie
from xdsl.dialects.builtin import Region, IndexType, ModuleOp, i32, IntegerAttr, ArrayAttr, i64, StringAttr
from xdsl.dialects.arith import Constant
from xdsl.dialects.memref import MemRefType
from xdsl.dialects import builtin, arith, memref, func
from xdsl.builder import Builder
from xdsl.traits import SymbolTable

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

    @Builder.region
    def region0(builder: Builder):
        builder.insert(tile14)
        builder.insert(tile34)
        builder.insert(object_fifo)
        builder.insert(lock34_8)
        
    device_val = IntegerAttr.from_int_and_width(0, i32)
    device = aie.DeviceOp(device_val, region0)

    acquire_fifo = aie.ObjectFifoAcquireOp(I32Attr(aie.PRODUCE_PORT), I32Attr(1), object_fifo.sym_name, device)
    
    @Builder.region
    def core14_region(builder: Builder):
        builder.insert(acquire_fifo)

    stackSize = IntegerAttr.from_int_and_width(1, i32)
    core14 = aie.CoreOp(stackSize, tile14, core14_region)


    region0.block.add_op(core14)

    subview = aie.ObjectFIFOSubviewAccessOp(I32Attr(0), acquire_fifo)
    core14.region.block.add_op(subview)

    module = builtin.ModuleOp([device])
    value_14 = Constant.from_int_and_width(14, i32)
    idx_3 = Constant.from_int_and_width(3, IndexType())
    memref_store = memref.Store.get(value_14, subview, idx_3)
    release_fifo = aie.ObjectFIFOReleaseOp(I32Attr(0), I32Attr(1), object_fifo.sym_name)

    core14.region.block.add_op(value_14)
    core14.region.block.add_op(idx_3)
    core14.region.block.add_op(memref_store)
    core14.region.block.add_op(release_fifo)
    core14.region.block.add_op(aie.EndOp())

    acquire_fifo = aie.ObjectFifoAcquireOp(I32Attr(aie.CONSUME_PORT), I32Attr(1), object_fifo.sym_name, device)
    
    @Builder.region
    def core34_region(builder: Builder):
        uselock34_8_acquire = aie.UseLockOp(I32Attr(0), I32Attr(aie.LOCK_ACQUIRE), I32Attr(1), lock34_8)
        builder.insert(uselock34_8_acquire)
        builder.insert(acquire_fifo)

    core34 = aie.CoreOp(stackSize, tile34, core34_region)

    subview = aie.ObjectFIFOSubviewAccessOp(I32Attr(0), acquire_fifo)
    idx_1 = Constant.from_int_and_width(3, IndexType())
    d1 = memref.Load.get(subview, idx_1)
    c1 = Constant.from_int_and_width(100, i32)
    d2 = arith.Addi(d1, c1)
    idx_2 = Constant.from_int_and_width(5, IndexType())
    store = memref.Store.get(d2, subview, idx_2)
    release_fifo = aie.ObjectFIFOReleaseOp(I32Attr(aie.CONSUME_PORT), I32Attr(1), object_fifo.sym_name)
    uselock34_8_release = aie.UseLockOp(I32Attr(1), I32Attr(aie.LOCK_RELEASE), I32Attr(1), lock34_8)

    core34.region.block.add_op(subview)
    core34.region.block.add_op(idx_1)
    core34.region.block.add_op(d1)
    core34.region.block.add_op(c1)
    core34.region.block.add_op(d2)
    core34.region.block.add_op(idx_2)
    core34.region.block.add_op(store)
    core34.region.block.add_op(release_fifo)
    core34.region.block.add_op(uselock34_8_release)
    core34.region.block.add_op(aie.EndOp())

    region0.block.add_op(core34)

    print(module)

if __name__ == "__main__":
    tutorial4()
