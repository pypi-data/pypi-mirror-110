# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBOutput

import tdw.flatbuffers

class SimpleTransform(object):
    __slots__ = ['_tab']

    # SimpleTransform
    def Init(self, buf, pos):
        self._tab = tdw.flatbuffers.table.Table(buf, pos)

    # SimpleTransform
    def Position(self, obj):
        obj.Init(self._tab.Bytes, self._tab.Pos + 0)
        return obj

    # SimpleTransform
    def Rotation(self, obj):
        obj.Init(self._tab.Bytes, self._tab.Pos + 12)
        return obj

    # SimpleTransform
    def Forward(self, obj):
        obj.Init(self._tab.Bytes, self._tab.Pos + 28)
        return obj


def CreateSimpleTransform(builder, position_x, position_y, position_z, rotation_x, rotation_y, rotation_z, rotation_w, forward_x, forward_y, forward_z):
    builder.Prep(4, 40)
    builder.Prep(4, 12)
    builder.PrependFloat32(forward_z)
    builder.PrependFloat32(forward_y)
    builder.PrependFloat32(forward_x)
    builder.Prep(4, 16)
    builder.PrependFloat32(rotation_w)
    builder.PrependFloat32(rotation_z)
    builder.PrependFloat32(rotation_y)
    builder.PrependFloat32(rotation_x)
    builder.Prep(4, 12)
    builder.PrependFloat32(position_z)
    builder.PrependFloat32(position_y)
    builder.PrependFloat32(position_x)
    return builder.Offset()
