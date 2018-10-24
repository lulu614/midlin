from mindlin import mindlin
from load_paramenter import load_paramenter,search_num

#导入参数
# num   编号
# x,y   坐标
# a     桩端阻力比
# b     沿桩身均匀分布的桩侧摩阻力比
# v     地基土的泊松比
# Q     单桩在竖向荷载的准永久组合作用下的附加荷载
# l     桩长
# r     计算点离桩身轴线的水平距离
# h     厚度
# Es    压缩模量
# v     泊松比
#桩参数   {num:[x,y,a,b,Q,l,d,[(h,Es,v),...]],...}

def stiffness(num):
    pile_dict_all = load_paramenter()
    pile_dict = search_num(num,pile_dict_all)
    # num_list = pile_dict.keys()


    soil_list = pile_dict[num][5]      #  去掉桩底以上部分--------------->未解决
    soil_size = len(soil_list)

    z = 0   #深度
    sum_s = 0   #沉降
    for i in range(soil_size):      #分土层计算

        soil_list_i = soil_list[i]

        #土层参数
        h = soil_list_i[0]
        Es = soil_list_i[1]
        v = soil_list_i[2]

        thickness = 2       #分层厚度-------可修改

        soil_list_i_size = h//thickness+1      #分层数
        h_last = h - (thickness*soil_list_i_size-1)        #最后一层厚度

        for j in range(soil_list_i_size):          #按thickness分层计算

            #判断是否是最后一层
            if j == soil_list_i_size-1:
                h_j = h_last
            else:
                h_j = thickness

            stress = 0   #附加应力值
            for k in pile_dict:
                # 桩参数
                a = pile_dict[k][0]  # 桩端阻力系数
                b = pile_dict[k][1]  # 沿桩身均匀分布荷载系数

                # 荷载参数
                Q = pile_dict[k][2]  # 单桩在竖向荷载的准永久组合作用下的附加荷载
                l = pile_dict[k][3]  # 长度
                r = pile_dict[k][6]-pile_dict[k][6]/2  #距离

                #计算并累加附加应力值
                m = mindlin(a, b, v, Q, l, r, z)
                stress += m[0] + m[1]

            sum_s += stress*h_j/Es   #累计沉降值
            z += h_j    #累计深度值

    Q = pile_dict[num][2]
    E = Q/sum_s*1000
    return E


#测试
#print(sedimentation(200))
