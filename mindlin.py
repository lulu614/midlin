from math import pi,log,sqrt

#明德林应力法求解

# a  桩端阻力比
# b  沿桩身均匀分布的桩侧摩阻力比
# v  地基土的泊松比
# Q  单桩在竖向荷载的准永久组合作用下的附加荷载
# r  计算点离桩身轴线的水平距离
# l  桩长
# z  计算应力点离承台底面的竖向距离

def mindlin(a,b,v,Q,l,r,z):


    #参数转换
    m = z/l
    n = r/l
    A = sqrt(n**2 + (m-1)**2)
    B = sqrt(n**2 + (m+1)**2)
    F = sqrt(n**2 + m**2)

    #计算应力影响系数

    #对于桩顶的集中力
    Ip = 1/(8*pi*(1-v))\
         * ((1-2*v)*(m-1)/A**3\
            - (1-2*v)*(m-1)/B**3\
            + 3*(m-1)**3/A**5\
            + (3*(3-4*v)*m*(m+1)**2-3*(m+1)*(5*m-1))/B**5\
            + 30*m*(m+1)**3/B**7)

    #对于桩侧摩阻力沿桩身均匀分布
    Is1 = 1/(8*pi*(1-v))\
          * (2*(2-v)/A\
             - (2*(2-v)+2*(1-2*v)*(m**2/n**2+m/n**2))/B\
             + (1-2*v)*2*(m/n)**2/F\
             - n**2/A**3
             - (4*m**2-4*(1+v)*(m/n)**2*m**2)/F**3\
             - (4*m*(1+v)*(m+1)*(m/n+1/n)**2-(4*m**2+n**2))/B**3\
             + 6*m**2*(m**4-n**4)/n**2/F**5\
             - 6*m*(m*n**2-(m+1)**5/n**2)/B**5)

    #对于桩侧摩阻力沿桩身均匀分布
    Is2 = 1/(4*pi*(1-v))\
          * (2*(2-v)/A\
             - (2*(2-v)*(4*m+1)-2*(1-2*v)*(1+m)*m**2/n**2)/B\
             - (2*(1-2*v)*m**3/n**2-8*(2-v)*m)/F\
             - (m*n**2+(m-1)**3)/A**3\
             - (4*v*n**2*m+4*m**3-15*n**2*m-2*(5+2*v)*(m/n)**2*(m+1)**3+(m+1)**3)/B**3\
             - (2*(7-2*v)*m*n**2-6*m**3+2*(5+2*v)*(m/n)**2*m**3)/F**3\
             - (6*m*n**2*(n**2-m**2)+12*(m/n)**2*(m+1)**5)/B**5\
             + (12*(m/n)**2*m**5+6*m*n**2*(n**2-m**2))/F**5\
             + 2*(2-v)*log((A+m-1)/(F+m)*(B+m+1)/(F+m)))


    print(Ip,Is1,Is2)

    #侧端阻力在深度z处产生的应力
    stress_tip =  a*Q/l**2*Ip
    # 侧摩阻力在深度z处产生的应力
    stress_side = Q/l**2*(b*Is1+(1-a-b)*Is2)
    return stress_tip,stress_side


#测试
# #     mindlin(a,  b,  v,  Q,   l,r, z):
value = mindlin(0.3,0,0.7,1389.108193,15,4,15)
print(value[0],value[1])


