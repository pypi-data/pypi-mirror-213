import pywavefront
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()

HEAD_OBJ = pywavefront.Wavefront(
    file_path.parent.parent.parent / "data" / "visual" / "head2.obj", collect_faces=True
)
HEAD_BOX = (HEAD_OBJ.vertices[0], HEAD_OBJ.vertices[0])
for vertex in HEAD_OBJ.vertices:
    min_v = [min(HEAD_BOX[0][i], vertex[i]) for i in range(3)]
    max_v = [max(HEAD_BOX[1][i], vertex[i]) for i in range(3)]
    HEAD_BOX = (min_v, max_v)

HEAD_OBJ_SIZE = [HEAD_BOX[1][i] - HEAD_BOX[0][i] for i in range(3)]
