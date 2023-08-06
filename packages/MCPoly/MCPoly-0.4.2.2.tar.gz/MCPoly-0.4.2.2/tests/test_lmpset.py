from MCPoly.lmpset import mould
import re
import os
import pytest

@pytest.fixture
def atoms():
    return mould('Poly1',loc='./data_lmpset/')

def test_cube(atoms):
    opath=os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.cube(6,5,6,5,3,5)
    os.chdir(opath)
    fl=open('./MCPoly/tests/data_lmpset/Poly1_663.data','r')
    i1=0
    i2=0
    i3=0
    i4=0
    i5=0
    i6=0
    i7=0
    i8=0
    i9=0
    for line in fl:
        a=re.search('972 atoms',line)
        if a:
            i1=1
        b=re.search('1404 angles',line)
        if b:
            i2=1
        c=re.search('432 impropers',line)
        if c:
            i3=1
        d=re.search('4 atom types',line)
        if d:
            i4=1
        e=re.search('4 bond types',line)
        if e:
            i5=1
        f=re.search('4 dihedral types',line)
        if f:
            i6=1
        g=re.search('0.00000 53.32948 xlo xhi',line)
        if g:
            i7=1
        h=re.search('0.00000 54.87382 ylo yhi',line)
        if h:
            i8=1
        i=re.search('0.00000 26.46613 zlo zhi',line)
        if i:
            i9=1
            break
    fl.close()
    assert i1*i2*i3*i4*i5*i6*i7*i8*i9!=0

@pytest.fixture
def atoms():
    return mould('Poly1',loc='./data_lmpset/')

def test_brick_xy(atoms):
    opath=os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.brick(6,5,6,5,4,5,xpattern='y')
    os.chdir(opath)
    fl=open('./MCPoly/tests/data_lmpset/Poly1_664_brickxy.data','r')
    i1=0
    i2=0
    i3=0
    i4=0
    i5=0
    i6=0
    i7=0
    i8=0
    i9=0
    for line in fl:
        a=re.search('1188 atoms',line)
        if a:
            i1=1
        b=re.search('1056 bonds',line)
        if b:
            i2=1
        c=re.search('1584 dihedrals',line)
        if c:
            i3=1
        d=re.search('4 atom types',line)
        if d:
            i4=1
        e=re.search('5 angle types',line)
        if e:
            i5=1
        f=re.search('1 improper types',line)
        if f:
            i6=1
        g=re.search('0.00000 53.32948 xlo xhi',line)
        if g:
            i7=1
        h=re.search('0.00000 54.87382 ylo yhi',line)
        if h:
            i8=1
        i=re.search('0.00000 36.95484 zlo zhi',line)
        if i:
            i9=1
            break
    fl.close()
    assert i1*i2*i3*i4*i5*i6*i7*i8*i9!=0

@pytest.fixture
def atoms():
    return mould('Poly1',loc='./data_lmpset/')

def test_brick_yz(atoms):
    opath=os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.brick(6,5,6,5,4,5,ypattern='z')
    os.chdir(opath)
    fl=open('./MCPoly/tests/data_lmpset/Poly1_664_brickyz.data','r')
    i1=0
    i2=0
    i3=0
    i4=0
    i5=0
    i6=0
    i7=0
    i8=0
    i9=0
    for line in fl:
        a=re.search('1134 atoms',line)
        if a:
            i1=1
        b=re.search('1008 bonds',line)
        if b:
            i2=1
        c=re.search('1512 dihedrals',line)
        if c:
            i3=1
        d=re.search('4 atom types',line)
        if d:
            i4=1
        e=re.search('5 angle types',line)
        if e:
            i5=1
        f=re.search('1 improper types',line)
        if f:
            i6=1
        g=re.search('0.00000 53.32948 xlo xhi',line)
        if g:
            i7=1
        h=re.search('0.00000 54.87382 ylo yhi',line)
        if h:
            i8=1
        i=re.search('0.00000 36.95484 zlo zhi',line)
        if i:
            i9=1
            break
    fl.close()
    assert i1*i2*i3*i4*i5*i6*i7*i8*i9!=0

@pytest.fixture
def atoms():
    return mould('Poly1',loc='./data_lmpset/')

def test_brick_zx(atoms):
    opath=os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.brick(6,5,6,5,4,5,zpattern='x')
    os.chdir(opath)
    fl=open('./MCPoly/tests/data_lmpset/Poly1_664_brickzx.data','r')
    i1=0
    i2=0
    i3=0
    i4=0
    i5=0
    i6=0
    i7=0
    i8=0
    i9=0
    for line in fl:
        a=re.search('1188 atoms',line)
        if a:
            i1=1
        b=re.search('1056 bonds',line)
        if b:
            i2=1
        c=re.search('1584 dihedrals',line)
        if c:
            i3=1
        d=re.search('4 atom types',line)
        if d:
            i4=1
        e=re.search('5 angle types',line)
        if e:
            i5=1
        f=re.search('1 improper types',line)
        if f:
            i6=1
        g=re.search('0.00000 53.32948 xlo xhi',line)
        if g:
            i7=1
        h=re.search('0.00000 54.87382 ylo yhi',line)
        if h:
            i8=1
        i=re.search('0.00000 36.95484 zlo zhi',line)
        if i:
            i9=1
            break
    fl.close()
    assert i1*i2*i3*i4*i5*i6*i7*i8*i9!=0

@pytest.fixture
def atoms():
    return mould('Poly1',loc='./data_lmpset/')

def test_DATAtoXYZ(atoms):
    opath=os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.DATAtoXYZ()
    os.chdir(opath)
    fl=open('./MCPoly/tests/data_lmpset/Poly1.xyz','r')
    i1=0
    i2=0
    i3=0
    i4=0
    for line in fl:
        a=re.match('9',line)
        if a:
            i1=1
        b=re.search('C       -7.66670000       0.30320000      -0.05380000',line)
        if b:
            i2=1
        c=re.search('O       -7.72351010       0.80779380       2.29626760',line)
        if c:
            i3=1
        d=re.search('H       -8.04585390      -0.09712450       2.44769150',line)
        if d:
            i4=1
            break
    fl.close()
    assert i1*i2*i3*i4!=0

@pytest.fixture
def atoms():
    return mould('Poly1',loc='./data_lmpset/')

def test1_DATAtomolTXT(atoms):
    opath=os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.DATAtomolTXT()
    os.chdir(opath)
    fl=open('./MCPoly/tests/data_lmpset/Poly1.txt','r')
    i1=0
    i2=0
    i3=1
    i4=0
    i5=0
    i6=0
    i7=0
    i8=0
    i9=0
    i10=0
    for line in fl:
        a=re.search('9 atoms',line)
        if a:
            i1=1
        b=re.search('12 dihedrals',line)
        if b:
            i2=1
        c=re.search('5 angle types',line)
        if c:
            i3=0
        d=re.search('Coords',line)
        if d:
            i4=1
        e=re.search('Types',line)
        if e:
            i5=1
        f=re.search('Charges',line)
        if f:
            i6=1
        g=re.search('Bonds',line)
        if g:
            i7=1
        h=re.search('Angles',line)
        if h:
            i8=1
        i=re.search('Dihedrals',line)
        if i:
            i9=1
        j=re.search('Impropers',line)
        if j:
            i10=1
            break
    fl.close()
    assert i1*i2*i3*i4*i5*i6*i7*i8*i9*i10!=0

def test2_DATAtomolTXT(atoms):
    opath=os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.DATAtomolTXT(types={1:11},savename='Poly1_2')
    os.chdir(opath)
    fl=open('./MCPoly/tests/data_lmpset/Poly1_2.txt','r')
    i1=0
    i2=0
    i3=0
    for line in fl:
        a=re.match('2 11',line)
        if a:
            i1=1
        b=re.match('5 2',line)
        if b:
            i2=1
        c=re.match('9 4',line)
        if c:
            i3=1
    fl.close()
    assert i1*i2*i3!=0

@pytest.fixture
def atoms():
    return mould('Poly2',loc='./data_lmpset/')

def test_infchain(atoms):
    opath=os.getcwd()
    os.chdir('./MCPoly/tests')
    atoms.infchain(3)
    os.chdir(opath)
    fl=open('./MCPoly/tests/data_lmpset/Poly2_Chain.txt','r')
    i1=0
    i2=0
    i3=1
    i4=0
    i5=0
    i6=0
    for line in fl:
        a=re.search('7 atoms',line)
        if a:
            i1=1
        b=re.search('9 angles',line)
        if b:
            i2=1
        c=re.search('2 impropers',line)
        if c:
            i3=0
        d=re.search('4 bond types',line)
        if d:
            i4=1
        e=re.search('4 dihedral types',line)
        if e:
            i5=1
        f=re.search('7 3 5 1',line)
        if f:
            i6=1
            break
    fl.close()
    assert i1*i2*i3*i4*i5*i6!=0

#def test_chain(atoms):
#    opath=os.getcwd()
#    os.chdir('./MCPoly/tests')
#    atoms.chain(3,5)
#    os.chdir(opath)
#    fl=open('./MCPoly/tests/data_lmpset/Poly2_Chain.txt','r')
#    i1=0
#    i2=0
#    i3=1
#    i4=0
#    i5=0
#    i6=0
#    for line in fl:
#        a=re.search('7 atoms',line)
#        if a:
#            i1=1
#        b=re.search('9 angles',line)
#        if b:
#            i2=1
#        c=re.search('2 impropers',line)
#        if c:
#            i3=0
#        d=re.search('4 bond types',line)
#        if d:
#            i4=1
#        e=re.search('4 dihedral types',line)
#        if e:
#            i5=1
#        f=re.search('7 3 5 1',line)
#        if f:
#            i6=1
#            break
#    fl.close()
#    assert i1*i2*i3*i4*i5*i6!=0