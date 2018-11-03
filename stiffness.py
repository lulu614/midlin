# -*- coding: gbk -*-

from mindlin import mindlin
from load_paramenter import load_paramenter,get_list

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
    pile_dict = get_list(num,pile_dict_all)
    # num_list = pile_dict.keys()

    #  去掉桩底以上部分--------------->未解决

    l = pile_dict[num][3]            #桩长
    soil_list = pile_dict[num][5]      #对应编号桩参数

    z = l   #深度
    sum_s = 0   #沉降
    for i in soil_list:      #分土层计算

        # 土层参数
        h = i[0]
        Es = i[1]
        v = i[2]

        #建立h_list ——分层列表
        thickness = 2  # 分层厚度-------可修改
        if isinstance(h/thickness,int):
            soil_list_i_size = h // thickness       #分层数
            h_list = soil_list_i_size*[thickness]
        else:
            soil_list_i_size = h//thickness+1
            h_last = h - (thickness*soil_list_i_size-1)        #最后一层厚度
            h_list = soil_list_i_size * [thickness]+[h_last]

        for h in h_list:          #按thickness分层计算

            stress = 0   #附加应力值
            for k in pile_dict:

                a = pile_dict[k][0]  # 桩端阻力系数
                b = pile_dict[k][1]  # 沿桩身均匀分布荷载系数
                Q = pile_dict[k][2]  # 单桩在竖向荷载的准永久组合作用下的附加荷载
                l = pile_dict[k][3]  # 长度
                r = pile_dict[k][6]  #距离

                #计算并累加附加应力值
                m = mindlin(a, b, v, Q, l, r, z)
                stress += m[0] + m[1]
                # print(a, b, v, Q, l, r, z)
                # print(m[0] , m[1])
                # print(stress)


            sum_s += stress*h/Es   #累计沉降值
            z += h    #累计深度值

    Q = pile_dict[num][2]
    E = Q/sum_s*1000
    return E


#测试
# print(stiffness(200))
