# in shell
import os, sys
simfempypath = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir, os.path.pardir,'simfempy'))
sys.path.insert(0,simfempypath)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pygmsh
from simfempy.applications.stokes import Stokes
from simfempy.applications.navierstokes import NavierStokes
from simfempy.applications.problemdata import ProblemData
from simfempy.meshes.simplexmesh import SimplexMesh
from simfempy.meshes import plotmesh

# ================================================================c#
def main(**kwargs):
    testcases = ['drivenCavity', 'backwardFacingStep', 'poiseuille', 'schaeferTurek']
    testcase = kwargs.pop('testcase', testcases[0])
    model = kwargs.pop('model', 'NavierStokes')
    bdryplot = kwargs.pop('bdryplot', False)
    linearsolver = kwargs.pop('linearsolver', 'umf')
    # create mesh and data
    mesh, data = eval(testcase)(**kwargs)
    if bdryplot: 
        plotmesh.meshWithBoundaries(mesh)
        plt.show()
        return
    # create application
    if model == "Stokes":
        model = Stokes(mesh=mesh, problemdata=data, linearsolver=linearsolver)
    else:
        model = NavierStokes(mesh=mesh, problemdata=data, linearsolver=linearsolver)
    result = model.solve()
    print(f"{result.info['timer']}")
    print(f"postproc:")
    for k, v in result.data['global'].items(): print(f"{k}: {-50*v}")
    fig = plt.figure(figsize=(10, 8))
    outer = gridspec.GridSpec(1, 2, wspace=0.2, hspace=0.2)
    # plotmesh.meshWithBoundaries(mesh, fig=fig, outer=outer[0])
    plotmesh.meshWithData(mesh, data=result.data, title="Stokes", fig=fig, outer=outer[0])
    plotmesh.meshWithData(mesh, title="Stokes", fig=fig, outer=outer[1],
                          quiver_data={"V":list(result.data['point'].values())})
    plt.show()


# ================================================================c#
def drivenCavity(h=0.1, mu=0.01):
    with pygmsh.geo.Geometry() as geom:
        ms = [h*v for v in [1.,1.,0.2,0.2]]
        p = geom.add_rectangle(xmin=0, xmax=1, ymin=0, ymax=1, z=0, mesh_size=ms)
        geom.add_physical(p.surface, label="100")
        for i in range(len(p.lines)): geom.add_physical(p.lines[i], label=f"{1000 + i}")
        mesh = geom.generate_mesh()
    data = ProblemData()
    # boundary conditions
    data.bdrycond.set("Dirichlet", [1000, 1001, 1002, 1003])
    # data.bdrycond.set("Dirichlet", [1002])
    # data.bdrycond.set("Navier", [1000, 1001, 1003])
    data.bdrycond.fct[1002] = [lambda x, y, z: 1, lambda x, y, z: 0]
    # parameters
    data.params.scal_glob["mu"] = mu
    data.params.scal_glob["navier"] = mu
    #TODO pass ncomp with mesh ?!
    data.ncomp = 2
    return SimplexMesh(mesh=mesh), data


# ================================================================ #
def backwardFacingStep(h=0.2, mu=0.02):
    with pygmsh.geo.Geometry() as geom:
        X = []
        X.append([-1.0, 1.0])
        X.append([-1.0, 0.0])
        X.append([0.0, 0.0])
        X.append([0.0, -1.0])
        X.append([3.0, -1.0])
        X.append([3.0, 1.0])
        p = geom.add_polygon(points=np.insert(np.array(X), 2, 0, axis=1), mesh_size=h)
        geom.add_physical(p.surface, label="100")
        for i in range(len(p.lines)): geom.add_physical(p.lines[i], label=f"{1000 + i}")
        mesh = geom.generate_mesh()
    data = ProblemData()
    # boundary conditions
    # data.bdrycond.set("Dirichlet", [1000, 1001, 1002, 1003])
    data.bdrycond.set("Dirichlet", [1000, 1001, 1002, 1003, 1005])
    # data.bdrycond.set("Neumann", [1004])
    data.bdrycond.set("Pressure", [1004])
    # data.bdrycond.set("Navier", [1005])
    # data.bdrycond.fct[1000] = [lambda x, y, z: 1,  lambda x, y, z: 0]
    data.bdrycond.fct[1000] = [lambda x, y, z: y*(1-y),  lambda x, y, z: 0]
    # parameters
    data.params.scal_glob["mu"] = mu
    data.params.scal_glob["navier"] = 0.1
    #TODO pass ncomp with mesh ?!
    data.ncomp = 2
    return SimplexMesh(mesh=mesh), data
# ================================================================ #
def poiseuille(h= 0.1, mu=0.1):
    with pygmsh.geo.Geometry() as geom:
        #ms = [h*v for v in [1.,1.,0.2,0.2]]
        ms = h
        p = geom.add_rectangle(xmin=-1.0, xmax=3.0, ymin=-1.0, ymax=1.0, z=0, mesh_size=ms)
        geom.add_physical(p.surface, label="100")
        for i in range(len(p.lines)): geom.add_physical(p.lines[i], label=f"{1000 + i}")
        mesh = geom.generate_mesh()
    data = ProblemData()
   # boundary conditions
    data.bdrycond.set("Dirichlet", [1002,1000,1003])
    data.bdrycond.set("Neumann", [])
    data.bdrycond.set("Navier", [])
    data.bdrycond.set("Pressure", [1001])
    data.bdrycond.fct[1003] = [lambda x, y, z:  1-y**2, lambda x, y, z: 0]
    # data.bdrycond.fct[1002] = [lambda x, y, z:  1, lambda x, y, z: 0]
    # data.bdrycond.fct[1003] = {'p': lambda x, y, z:  1}
    # data.bdrycond.fct[1003] = [lambda x, y, z, nx, ny, nz:  1, lambda x, y, z, nx, ny, nz:  0]
    #--------------------------------------------------------------------------
    #navier_slip_boundary
    # data.bdrycond.fct[1000] = { 'g': [lambda x, y, z:  1, lambda x, y, z:  0]}
    #---------------------------------------------------------------------------
    # parameters
    data.params.scal_glob["mu"] = mu
    data.params.scal_glob["navier"] = 1.01
    #TODO pass ncomp with mesh ?!
    data.ncomp = 2
    return SimplexMesh(mesh=mesh), data
# ================================================================ #
def schaeferTurek(h= 0.5, mu=0.01, hcircle=None):
    if hcircle is None: hcircle = 0.2*h
    with pygmsh.geo.Geometry() as geom:
        circle = geom.add_circle(x0=[2,2], radius=0.5, mesh_size=hcircle, num_sections=10, make_surface=False)
        geom.add_physical(circle.curve_loop.curves, label="3000")
        p = geom.add_rectangle(xmin=0, xmax=11, ymin=0, ymax=4.1, z=0, mesh_size=h, holes=[circle])
        geom.add_physical(p.surface, label="100")
        for i in range(len(p.lines)): geom.add_physical(p.lines[i], label=f"{1000 + i}")
        mesh = geom.generate_mesh()
    data = ProblemData()
   # boundary conditions
    data.bdrycond.set("Dirichlet", [1002,1000,1003,3000])
    data.bdrycond.set("Neumann", [1001])
    data.bdrycond.fct[1003] = [lambda x, y, z:  0.3*y*(4.1-y)/2.05**2, lambda x, y, z: 0]
    data.params.scal_glob["mu"] = mu
    data.postproc.set(name='bdrynflux', type='bdry_nflux', colors=3000)
    #TODO pass ncomp with mesh ?!
    data.ncomp = 2
    return SimplexMesh(mesh=mesh), data

#================================================================#
if __name__ == '__main__':
    main(testcase='poiseuille', h=0.2, mu=1e-3)
    main(testcase='drivenCavity', mu=3e-4)
    main(testcase='backwardFacingStep', mu=2e-3)
    main(testcase='schaeferTurek', h=0.5, hcircle=0.1, mu=0.01)
