# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBOutput

import tdw.flatbuffers

class SegmentationColorData(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsSegmentationColorData(cls, buf, offset):
        n = tdw.flatbuffers.encode.Get(tdw.flatbuffers.packer.uoffset, buf, offset)
        x = SegmentationColorData()
        x.Init(buf, n + offset)
        return x

    # SegmentationColorData
    def Init(self, buf, pos):
        self._tab = tdw.flatbuffers.table.Table(buf, pos)

    # SegmentationColorData
    def Id(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # SegmentationColorData
    def SegmentationColor(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from .Color import Color
            obj = Color()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # SegmentationColorData
    def Name(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def SegmentationColorDataStart(builder): builder.StartObject(3)
def SegmentationColorDataAddId(builder, id): builder.PrependInt32Slot(0, id, 0)
def SegmentationColorDataAddSegmentationColor(builder, segmentationColor): builder.PrependStructSlot(1, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(segmentationColor), 0)
def SegmentationColorDataAddName(builder, name): builder.PrependUOffsetTRelativeSlot(2, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(name), 0)
def SegmentationColorDataEnd(builder): return builder.EndObject()
