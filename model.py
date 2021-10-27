import numpy

class Model:
    def __init__(self, filename):
        self.vertices = []
        self.uv_vertices = []#贴图
        self.uv_indices = []
        self.indices = []#对应哪三个顶点构成一个面，从1开始


        with open(filename) as f:
            for line in f:
                if line.startswith("v "):
                    x, y, z = [float(d) for d in line.strip("v").strip().split(" ")]
                    self.vertices.append(numpy.array([x, y, z, 1]))
                elif line.startswith("vt "):
                    u, v = [float(d) for d in line.strip("vt").strip().split(" ")]
                    self.uv_vertices.append([u, v])
                elif line.startswith("f "):
                    facet = [d.split("/") for d in line.strip("f").strip().split(" ")]
                    self.indices.append([int(d[0]) for d in facet])
                    self.uv_indices.append([int(d[1]) for d in facet])
                    

if __name__=="__main__":
    m=Model("model/axe.obj")
    
    print("indices:")
    for i,j in enumerate(m.indices):
        print(i,j)
        if i>=10:   break
        
    print("vertices:")
    for i,j in enumerate(m.vertices):
        print(i,j)
        if i>=10:   break
        
    print("uv_indices:")
    for i,j in enumerate(m.uv_indices):
        print(i,j)
        if i>=10:   break
        
    print("uv_vertices:")
    for i,j in enumerate(m.uv_vertices):
        print(i,j)
        if i>=10:   break
        
    
