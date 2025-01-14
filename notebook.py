import marimo

__generated_with = "0.9.17"
app = marimo.App()


@app.cell
def __(mo):
    mo.md("""6#3D Geometry File Formats""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## About STL

        STL is a simple file format which describes 3D objects as a collection of triangles.
        The acronym STL stands for "Simple Triangle Language", "Standard Tesselation Language" or "STereoLitography"[^1].

        [^1]: STL was invented for – and is still widely used – for 3D printing.
        """
    )
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/teapot.stl", theta=45.0, phi=30.0, scale=2))
    return


@app.cell
def __(mo):
    with open("data/teapot.stl", mode="rt", encoding="utf-8") as _file:
        teapot_stl = _file.read()

    teapot_stl_excerpt = teapot_stl[:723] + "..." + teapot_stl[-366:]

    mo.md(
        f"""
    ## STL ASCII Format

    The `data/teapot.stl` file provides an example of the STL ASCII format. It is quite large (more than 60000 lines) and looks like that:
    """
    +
    f"""```
    {teapot_stl_excerpt}
    ```
    """
    +

    """
    """
    )
    return teapot_stl, teapot_stl_excerpt


@app.cell
def __(mo):
    mo.md(f"""

      - Study the [{mo.icon("mdi:wikipedia")} STL (file format)](https://en.wikipedia.org/wiki/STL_(file_format)) page (or other online references) to become familiar the format.

      - Create a STL ASCII file `"data/cube.stl"` that represents a cube of unit length  
        (💡 in the simplest version, you will need 12 different facets).

      - Display the result with the function `show` (make sure to check different angles).
    """)
    return


@app.cell
def __(show):
    # les sommets
    vertices = [
        (-0.5, -0.5, -0.5),
        (0.5, -0.5, -0.5),
        (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (-0.5, -0.5, 0.5),
        (0.5, -0.5, 0.5),
        (0.5, 0.5, 0.5),
        (-0.5, 0.5, 0.5),
    ]

    # les faces, à chaque fois deux triangles pour chaque face
    faces = [
        # devant
        (0, 1, 2, 0, 0, -1),
        (0, 2, 3, 0, 0, -1),

        # derrière
        (4, 5, 6, 0, 0, 1),
        (4, 6, 7, 0, 0, 1),

        # gauche
        (0, 3, 7, -1, 0, 0),
        (0, 7, 4, -1, 0, 0),

        # droite
        (1, 5, 6, 1, 0, 0),
        (1, 6, 2, 1, 0, 0),

        # haut
        (3, 2, 6, 0, 1, 0),
        (3, 6, 7, 0, 1, 0),

        # bas
        (0, 1, 5, 0, -1, 0),
        (0, 5, 4, 0, -1, 0),
    ]


    def create_cube_stl(filename):
        with open(filename, 'w') as file:
            file.write("solid cube\n")
            for face in faces:
                v1, v2, v3, nx, ny, nz = face
                file.write(f"facet normal {nx} {ny} {nz}\n")
                file.write("  outer loop\n")
                file.write(f"    vertex {vertices[v1][0]} {vertices[v1][1]} {vertices[v1][2]}\n")
                file.write(f"    vertex {vertices[v2][0]} {vertices[v2][1]} {vertices[v2][2]}\n")
                file.write(f"    vertex {vertices[v3][0]} {vertices[v3][1]} {vertices[v3][2]}\n")
                file.write("  endloop\n")
                file.write("endfacet\n")
            file.write("endsolid cube\n")

    # Create the STL file for the cube
    create_cube_stl("data/cube.stl")
    show("data/cube.stl", theta=45.0, phi=10.0, scale=1)

    return create_cube_stl, faces, vertices


@app.cell
def __(mo):
    mo.md(r"""## STL & NumPy""")
    return


@app.cell
def __(np):
    def normale(A, B, C):
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)

        # en suivant la règle de la main droite et en normalisant le vecteur normal
        AB = B - A
        AC = C - A
        normale = np.cross(AB, AC)
        norme = np.linalg.norm(normale)
        if norme != 0:
            normale = normale / norme

        return normale

    def make_STL(triangles, normals= None, name = ""):
        solid = "solid" + name
        n = len(triangles)
        for k in range (n):
            solid = solid +"\n \t facet normal "
            # on s'occupe de la normale 
            if normals == None : 
                n = normale(triangles[k][0],triangles[k][1],triangles[k][2])
                for x in n:
                    solid = solid + " " + str(x)
            else : 
                for x in normals[k]:
                    solid = solid + " " + str(x)
            solid += "\n \t \t outer loop "
            for l in triangles[k]:
                l = [str(x) for x in l ]
                solid = solid + "\n \t \t \t vertex " + " ".join(l)

            solid += " \n \t \t end of loop "
            solid += " \n \t endfacet "
        solid += "\n endsolid " + name
        
        return solid
    file = make_STL( [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
        ],None, )

    print(file)
    return file, make_STL, normale


@app.cell
def __(mo):
    mo.md(rf"""

    ### NumPy to STL

    Implement the following function:

    ```python
    def make_STL(triangles, normals=None, name=""):
        pass # 🚧 TODO!
    ```

    #### Parameters

      - `triangles` is a NumPy array of shape `(n, 3, 3)` and data type `np.float32`,
         which represents a sequence of `n` triangles (`triangles[i, j, k]` represents 
         is the `k`th coordinate of the `j`th point of the `i`th triangle)

      - `normals` is a NumPy array of shape `(n, 3)` and data type `np.float32`;
         `normals[i]` represents the outer unit normal to the `i`th facet.
         If `normals` is not specified, it should be computed from `triangles` using the 
         [{mo.icon("mdi:wikipedia")} right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule).

      - `name` is the (optional) solid name embedded in the STL ASCII file.

    #### Returns

      - The STL ASCII description of the solid as a string.

    #### Example

    Given the two triangles that make up a flat square:

    ```python

    square_triangles = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    )
    ```

    then printing `make_STL(square_triangles, name="square")` yields
    ```
    solid square
      facet normal 0.0 0.0 1.0
        outer loop
          vertex 0.0 0.0 0.0
          vertex 1.0 0.0 0.0
          vertex 0.0 1.0 0.0
        endloop
      endfacet
      facet normal 0.0 0.0 1.0
        outer loop
          vertex 1.0 1.0 0.0
          vertex 0.0 1.0 0.0
          vertex 1.0 0.0 0.0
        endloop
      endfacet
    endsolid square
    ```

    """)
    return


@app.cell
def __(np):
    def tokenize(stl):
        lines = stl.split("\n")
        tok = []
        for x in lines : 
            l = x.split(" ")
            for el in l : 
                if el != '':
                    if '.' in el : 
                        tok.append(np.float32(el))
                    else :
                        tok.append(el)
        return tok


    with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
        square_stl = square_file.read()
    tokens = tokenize(square_stl)


    if tokens == ['solid', 'square', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(0.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'endloop', 'endfacet', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(1.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'endloop', 'endfacet', 'endsolid', 'square']: 
        print("fonction réussie")
    return square_file, square_stl, tokenize, tokens


@app.cell
def __(mo):
    mo.md(
        """
        ### STL to NumPy

        Implement a `tokenize` function


        ```python
        def tokenize(stl):
            pass # 🚧 TODO!
        ```

        that is consistent with the following documentation:


        #### Parameters

          - `stl`: a Python string that represents a STL ASCII model.

        #### Returns

          - `tokens`: a list of STL keywords (`solid`, `facet`, etc.) and `np.float32` numbers.

        #### Example

        For the ASCII representation the square `data/square.stl`, printing the tokens with

        ```python
        with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
            square_stl = square_file.read()
        tokens = tokenize(square_stl)
        print(tokens)
        ```

        yields

        ```python
        ['solid', 'square', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(0.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'endloop', 'endfacet', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(1.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'endloop', 'endfacet', 'endsolid', 'square']
        ```
        """
    )
    return


@app.cell
def __(np, tokens):
    def parse(tokens):
        normals = []
        triangles = []
        name = tokens[1]
        k = 0
        while k < len(tokens) : 
            if tokens[k] == 'normal':
                normals.append(tokens[k+1:k+4])
                k = k+3
            if tokens[k] == 'loop' :
                triangles.append([tokens[k+2:k+5],tokens[k+6:k+9],tokens[k+10:k+13]])
                k=k+12
            k+=1

        normals = np.array(normals, dtype = np.float32)
        triangles = np.array(triangles, dtype = np.float32)


        return triangles, normals, name

    triangles, normals, name = parse(tokens)
    print(repr(triangles))
    print(repr(normals))
    print(repr(name))
    return name, normals, parse, triangles


@app.cell
def __(mo):
    mo.md(
        """
        Implement a `parse` function


        ```python
        def parse(tokens):
            pass # 🚧 TODO!
        ```

        that is consistent with the following documentation:


        #### Parameters

          - `tokens`: a list of tokens

        #### Returns

        A `triangles, normals, name` triple where

          - `triangles`: a `(n, 3, 3)` NumPy array with data type `np.float32`,

          - `normals`: a `(n, 3)` NumPy array with data type `np.float32`,

          - `name`: a Python string.

        #### Example

        For the ASCII representation `square_stl` of the square,
        tokenizing then parsing

        ```python
        with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
            square_stl = square_file.read()
        tokens = tokenize(square_stl)
        triangles, normals, name = parse(tokens)
        print(repr(triangles))
        print(repr(normals))
        print(repr(name))
        ```

        yields

        ```python
        array([[[0., 0., 0.],
                [1., 0., 0.],
                [0., 1., 0.]],

               [[1., 1., 0.],
                [0., 1., 0.],
                [1., 0., 0.]]], dtype=float32)
        array([[0., 0., 1.],
               [0., 0., 1.]], dtype=float32)
        'square'
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        rf"""
    ## Rules & Diagnostics



        Make diagnostic functions that check whether a STL model satisfies the following rules

          - **Positive octant rule.** All vertex coordinates are non-negative.

          - **Orientation rule.** All normals are (approximately) unit vectors and follow the [{mo.icon("mdi:wikipedia")} right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule).

          - **Shared edge rule.** Each triangle edge appears exactly twice.

          - **Ascending rule.** the z-coordinates of (the barycenter of) each triangle are a non-decreasing sequence.

    When the rule is broken, make sure to display some sensible quantitative measure of the violation (in %).

    For the record, the `data/teapot.STL` file:

      - 🔴 does not obey the positive octant rule,
      - 🟠 almost obeys the orientation rule, 
      - 🟢 obeys the shared edge rule,
      - 🔴 does not obey the ascending rule.

    Check that your `data/cube.stl` file does follow all these rules, or modify it accordingly!

    """
    )
    return


@app.cell
def __(parse, teapot_stl, tokenize):
    def pos_octant(stl):
        triangles, normals, name = parse(tokenize(stl))

        octant = True
        v = []
        s = 0
        for l in triangles : 
            for x in l :
                for e in x : 
                    if e not in v:
                        v.append(e)
                        if e <0:
                            s+=1
                            octant = False 
        return octant, f"pourcentage de violation de la règle : {100*s/len(v)}%"

    print(pos_octant(teapot_stl))
    return (pos_octant,)


@app.cell
def __(np, parse, teapot_stl, tokenize):
    def orientation_rule(stl):
        triangles, normals, name = parse(tokenize(stl))
        orientation = True
        s = 0
        for n in normals: 
            if abs(np.linalg.norm(n)-1) > 10e-8 :
                s+=1
                orientation = False
        return orientation, f"pourcentage de violation de la règle : {100*s/len(normals)} %"

    print(orientation_rule(teapot_stl))
    return (orientation_rule,)


@app.cell
def __():
    print({1,0} == {0,1})
    return


@app.cell
def __(parse, teapot_stl, tokenize):
    from collections import Counter
    def edges_of_triangle(triangle):

        edges = {tuple(sorted([tuple(triangle[i]), tuple(triangle[(i + 1) % 3])]))
            for i in range(3)}
        return edges


    def shared_edge_rule(stl):
        s = 0
        shared = True 
        triangles, normals, name = parse(tokenize(stl))

        edge_counter = Counter()

        # Loop over each triangle in the list of triangles.
        for triangle in triangles:
            edges = edges_of_triangle(triangle)
            edge_counter.update(edges)

        # Check if each edge appears exactly twice.
        for edge, count in edge_counter.items():
            if count != 2:
                shared = False 
                s+=1 

        return shared, f"pourcentage de violation de la règle : {100*s/len(edge_counter)}%"

    print(shared_edge_rule(teapot_stl))
    return Counter, edges_of_triangle, shared_edge_rule


@app.cell
def __(parse, teapot_stl, tokenize):
    def ascending_rule(stl):
        triangles, normals, name = parse(tokenize(stl))
        ascending = True
        s= 0 

        a,b,c = triangles[0]
        z_moy = (a[-1]+b[-1]+c[-1])/3
        for tri in triangles : 
            if (tri[0][-1]+tri[1][-1]+tri[2][-1])/3 >= z_moy : 
                z_moy = (tri[0][-1]+tri[1][-1]+tri[2][-1])/3
            else : 
                z_moy = (tri[0][-1]+tri[1][-1]+tri[2][-1])/3
                s+=1
                ascending = False
        return ascending, f"pourcentage de violation de la règle : {100*s/len(triangles)}%"

    print(ascending_rule(teapot_stl))
    return (ascending_rule,)


@app.cell
def __(mo):
    mo.md(
    rf"""
    ## OBJ Format

    The OBJ format is an alternative to the STL format that looks like this:

    ```
    # OBJ file format with ext .obj
    # vertex count = 2503
    # face count = 4968
    v -3.4101800e-003 1.3031957e-001 2.1754370e-002
    v -8.1719160e-002 1.5250145e-001 2.9656090e-002
    v -3.0543480e-002 1.2477885e-001 1.0983400e-003
    v -2.4901590e-002 1.1211138e-001 3.7560240e-002
    v -1.8405680e-002 1.7843055e-001 -2.4219580e-002
    ...
    f 2187 2188 2194
    f 2308 2315 2300
    f 2407 2375 2362
    f 2443 2420 2503
    f 2420 2411 2503
    ```

    This content is an excerpt from the `data/bunny.obj` file.

    """
    )
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/bunny.obj", scale="1.5"))
    return


@app.cell
def __(mo):
    mo.md(
        """
        Study the specification of the OBJ format (search for suitable sources online),
        then develop a `OBJ_to_STL` function that is rich enough to convert the OBJ bunny file into a STL bunny file.
        """
    )
    return


@app.cell
def __(make_STL, np):
    def OBJ_to_STL(obj):
        vertices = []
        triangles = []
        l_obj = obj.split("\n")
        for k in range (len(l_obj)):
            if len(l_obj[k]) !=0:  
                if l_obj[k][0] == "v": # on identifie de cette manière si c'est une vertice
                    v = l_obj[k].split(" ")
                    vertices.append(np.float32(v[1:]))
                elif l_obj[k][0] == "f": # et de cette manière on identifie si c'est une face
                    f = l_obj[k].split(" ")
                    triangles.append( [vertices[int(f[1])-1],vertices[int(f[2])-1],vertices[int(f[3])-1]])
        return make_STL(triangles, None, "bunny")

    with open("data/bunny.obj", mode="rt", encoding="us-ascii") as bunny_file:
        bunny_obj = bunny_file.read()
    bunny_STL = OBJ_to_STL(bunny_obj)
    print(bunny_STL[:200])
    return OBJ_to_STL, bunny_STL, bunny_file, bunny_obj


@app.cell
def __(mo):
    mo.md(
        rf"""
    ## Binary STL

    Since the STL ASCII format can lead to very large files when there is a large number of facets, there is an alternate, binary version of the STL format which is more compact.

    Read about this variant online, then implement the function

    ```python
    def STL_binary_to_text(stl_filename_in, stl_filename_out):
        pass  # 🚧 TODO!
    ```

    that will convert a binary STL file to a ASCII STL file. Make sure that your function works with the binary `data/dragon.stl` file which is an example of STL binary format.

    💡 The `np.fromfile` function may come in handy.

        """
    )
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/dragon.stl", theta=75.0, phi=-20.0, scale=1.7))
    return


@app.cell
def __(make_STL, np):
    def STL_binary_to_text(stl_filename_in, stl_filename_out):
        with open(stl_filename_in, mode="rb") as file:
            _ = file.read(80)
            n = np.fromfile(file, dtype=np.uint32, count=1)[0]
            normals = []
            faces = []
            for i in range(n):
                normals.append(np.fromfile(file, dtype=np.float32, count=3))
                faces.append(np.fromfile(file, dtype=np.float32, count=9).reshape(3, 3))
                _ = file.read(2)
        stl_text = make_STL(faces, normals)
        with open(stl_filename_out, mode="wt", encoding="utf-8") as file:
            file.write(stl_text)
    return (STL_binary_to_text,)


@app.cell
def __(mo):
    mo.md(rf"""## Constructive Solid Geometry (CSG)

    Have a look at the documentation of [{mo.icon("mdi:github")}fogleman/sdf](https://github.com/fogleman/) and study the basics. At the very least, make sure that you understand what the code below does:
    """)
    return


@app.cell
def __(X, Y, Z, box, cylinder, mo, show, sphere):
    demo_csg = sphere(1) & box(1.5)
    _c = cylinder(0.5)
    demo_csg = demo_csg - (_c.orient(X) | _c.orient(Y) | _c.orient(Z))
    demo_csg.save('output/demo-csg.stl', step=0.05)
    mo.show_code(show("output/demo-csg.stl", theta=45.0, phi=45.0, scale=1.0))
    return (demo_csg,)


@app.cell
def __(mo):
    mo.md("""ℹ️ **Remark.** The same result can be achieved in a more procedural style, with:""")
    return


@app.cell
def __(
    box,
    cylinder,
    difference,
    intersection,
    mo,
    orient,
    show,
    sphere,
    union,
):
    demo_csg_alt = difference(
        intersection(
            sphere(1),
            box(1.5),
        ),
        union(
            orient(cylinder(0.25), [1.0, 0.0, 0.0]),
            orient(cylinder(0.25), [0.0, 1.0, 0.0]),
            orient(cylinder(0.25), [0.0, 0.0, 1.0]),
        ),
    )
    demo_csg_alt.save("output/demo-csg-alt.stl", step=0.05)
    mo.show_code(show("output/demo-csg-alt.stl", theta=45.0, phi=45.0, scale=1.0))
    return (demo_csg_alt,)


@app.cell
def __():
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        rf"""
    ## JupyterCAD

    [JupyterCAD](https://github.com/jupytercad/JupyterCAD) is an extension of the Jupyter lab for 3D geometry modeling.

      - Use it to create a JCAD model that correspond closely to the `output/demo_csg` model;
    save it as `data/demo_jcad.jcad`.

      - Study the format used to represent JupyterCAD files (💡 you can explore the contents of the previous file, but you may need to create some simpler models to begin with).

      - When you are ready, create a `jcad_to_stl` function that understand enough of the JupyterCAD format to convert `"data/demo_jcad.jcad"` into some corresponding STL file.
    (💡 do not tesselate the JupyterCAD model by yourself, instead use the `sdf` library!)


        """
    )
    return


@app.cell
def __(
    box,
    cylinder,
    difference,
    intersection,
    orient,
    sphere,
    trimesh,
    union,
):
    def jcad_to_stl(file):
        csg = dict()
        csg["inter"]= []
        csg["union"]= []
        csg["diff"]= []
        for obj in file["objects"]:
            if obj["name"].startswith("Box"):
                l = obj["Height"]
                ax = obj["Axis"]
                csg[obj["name"]] = orient(box(l),ax)
            elif obj["name"].startswith("Cylinder"):
                ax = obj["Axis"]
                r = obj["Height"]
                csg[obj["name"]] = orient(cylinder(r),ax)
            elif obj["name"].startswith("Sphere"):
                r = obj["Radius"]
                csg[obj["name"]] = orient(sphere(r),ax)
            elif obj["name"].startswith("Intersection"):
                csg["inter"].append(obj["dependencies"])
            elif obj["name"].startswith("Union"):
                csg["Union"].append(obj["dependencies"])
            elif obj["name"].startswith("Difference"):
                csg["diff"].append(obj["dependencies"])

        csg_file = None
        for obj in csg.values() : 
            if csg_file != None : 
                break
            csg_file = obj

        for l in csg["inter"]: 
            csg_file = union(csg_file, intersection(csg[l[0]]),csg[l[1]])
        for l in csg["union"]: 
            csg_file = union(csg_file, union(csg[l[0]]),csg[l[1]])
        for l in csg["diff"]: 
            csg_file = union(csg_file, difference(csg[l[0]]),csg[l[1]])

        mesh = csg_file.to_mesh()
        mesh_trimesh = trimesh.Trimesh(vertices=mesh.vertices, faces=mesh.faces)

        # Sauvegarder le maillage en fichier STL
        mesh_trimesh.export(str(file)+'.stl')
        

    jcad_to_stl("untitled2.jcad")
    return (jcad_to_stl,)


@app.cell
def __(mo):
    mo.md("""## Appendix""")
    return


@app.cell
def __(mo):
    mo.md("""### Dependencies""")
    return


@app.cell
def __():
    # Python Standard Library
    import json

    # Marimo
    import marimo as mo

    # Third-Party Librairies
    import numpy as np
    import matplotlib.pyplot as plt
    import mpl3d
    from mpl3d import glm
    from mpl3d.mesh import Mesh
    from mpl3d.camera import Camera

    import meshio

    np.seterr(over="ignore")  # 🩹 deal with a meshio false warning

    import sdf
    from sdf import sphere, box, cylinder
    from sdf import X, Y, Z
    from sdf import intersection, union, orient, difference

    mo.show_code()
    return (
        Camera,
        Mesh,
        X,
        Y,
        Z,
        box,
        cylinder,
        difference,
        glm,
        intersection,
        json,
        meshio,
        mo,
        mpl3d,
        np,
        orient,
        plt,
        sdf,
        sphere,
        union,
    )


@app.cell
def __(sdf):
    help(sdf.box)
    return


@app.cell
def __(mo):
    mo.md(r"""### STL Viewer""")
    return


@app.cell
def __(Camera, Mesh, glm, meshio, mo, plt):
    def show(
        filename,
        theta=0.0,
        phi=0.0,
        scale=1.0,
        colormap="viridis",
        edgecolors=(0, 0, 0, 0.25),
        figsize=(6, 6),
    ):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1], xlim=[-1, +1], ylim=[-1, +1], aspect=1)
        ax.axis("off")
        camera = Camera("ortho", theta=theta, phi=phi, scale=scale)
        mesh = meshio.read(filename)
        vertices = glm.fit_unit_cube(mesh.points)
        faces = mesh.cells[0].data
        vertices = glm.fit_unit_cube(vertices)
        mesh = Mesh(
            ax,
            camera.transform,
            vertices,
            faces,
            cmap=plt.get_cmap(colormap),
            edgecolors=edgecolors,
        )
        return mo.center(fig)

    mo.show_code()
    return (show,)


@app.cell
def __(mo, show):
    mo.show_code(show("data/teapot.stl", theta=55.0, phi=30.0, scale=2))
    return


if __name__ == "__main__":
    app.run()
