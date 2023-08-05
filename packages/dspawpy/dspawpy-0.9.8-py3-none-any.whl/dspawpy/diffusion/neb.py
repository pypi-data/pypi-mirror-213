import os

from dspawpy.diffusion.pathfinder import IDPPSolver
from dspawpy.io.write import to_file


class NEB:
    """NEB插值算法

    Parameters
    ----------
    initial_structure: Structure
        初态
    final_structure: Structure
        终态
    nimages: int
        中间构型数
    """

    def __init__(self, initial_structure, final_structure, nimages):
        """

        Args:
            initial_structure:
            final_structure:
            nimages: number of images,contain initial and final structure
        """

        self.nimages = nimages
        self.iddp = IDPPSolver.from_endpoints(
            endpoints=[initial_structure, final_structure],
            nimages=self.nimages - 2,
            sort_tol=0,  # 锁定原子编号
        )

    def linear_interpolate(self):
        return self.iddp.structures

    def idpp_interpolate(
        self,
        maxiter=1000,
        tol=1e-5,
        gtol=1e-3,
        step_size=0.05,
        max_disp=0.05,
        spring_const=5.0,
    ):
        return self.iddp.run(maxiter, tol, gtol, step_size, max_disp, spring_const)


def write_neb_structures(
    structures,
    coords_are_cartesian=True,
    fmt: str = "as",
    path: str = ".",
    prefix="structure",
):
    r"""插值并生成中间构型文件

    Parameters
    ----------
    structures: list
        构型列表
    coords_are_cartesian: bool
        坐标是否为笛卡尔坐标
    fmt: str
        结构文件类型，默认为 "as"
    path: str
        保存路径
    prefix: str
        文件名前缀，默认为 "structure"，这样的话生成的就是 structure00.as, structure01.as, ...

    Returns
    -------
    file
        保存构型文件

    Examples
    --------

    先读取as文件创建structure对象

    >>> from dspawpy.io.structure import build_Structures_from_datafile
    >>> from dspawpy.diffusion.nebtools import write_movie_json

    >>> init_struct = build_Structures_from_datafile("/data/home/hzw1002/dspawpy_repo/test/2.15/00/structure00.as")[0]
    >>> final_struct = build_Structures_from_datafile("/data/home/hzw1002/dspawpy_repo/test/2.15/04/structure04.as")[0]

    然后，插值并生成中间构型文件

    >>> from dspawpy.diffusion.neb import NEB,write_neb_structures
    >>> neb = NEB(init_struct,final_struct,8)
    >>> structures = neb.linear_interpolate()   #线性插值

    插值完成的构型可指定保存到neb文件夹下

    >>> write_neb_structures(structures, fmt="as", path="/data/home/hzw1002/dspawpy_repo/test/out/11neb_interpolate_structures")
    --> 成功写入文件 /data/home/hzw1002/dspawpy_repo/test/out/11neb_interpolate_structures/00/structure00.as
    --> 成功写入文件 /data/home/hzw1002/dspawpy_repo/test/out/11neb_interpolate_structures/01/structure01.as
    --> 成功写入文件 /data/home/hzw1002/dspawpy_repo/test/out/11neb_interpolate_structures/02/structure02.as
    --> 成功写入文件 /data/home/hzw1002/dspawpy_repo/test/out/11neb_interpolate_structures/03/structure03.as
    --> 成功写入文件 /data/home/hzw1002/dspawpy_repo/test/out/11neb_interpolate_structures/04/structure04.as
    --> 成功写入文件 /data/home/hzw1002/dspawpy_repo/test/out/11neb_interpolate_structures/05/structure05.as
    --> 成功写入文件 /data/home/hzw1002/dspawpy_repo/test/out/11neb_interpolate_structures/06/structure06.as
    --> 成功写入文件 /data/home/hzw1002/dspawpy_repo/test/out/11neb_interpolate_structures/07/structure07.as
    """
    assert fmt is not None
    N = len(str(len(structures)))
    if N <= 2:
        N = 2
    for i, structure in enumerate(structures):
        path_name = str(i).zfill(N)
        os.makedirs(os.path.join(path, path_name), exist_ok=True)
        filename = os.path.join(path, path_name, "%s%s.%s" % (prefix, path_name, fmt))
        to_file(structure, filename, fmt, coords_are_cartesian)
