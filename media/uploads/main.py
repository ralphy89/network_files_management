def triangle(n):
    for i in range(1, n+1):
        print(i*'*')
        if i == n:
            for j in range(n, -1, -1):
                print(j*'*')

'''
    *
   ***
  *****
 *******
*********
'''

def christmasTree(height):
    space = height//2
    for i in range(1, height+1, 2):
        print(space*" "+ i*'*')
        space = space - 1
    return

christmasTree(10)
