# -*- coding: gbk -*-

from mindlin import mindlin
from load_paramenter import load_paramenter,get_list

#�������
# num   ���
# x,y   ����
# a     ׮��������
# b     ��׮����ȷֲ���׮��Ħ������
# v     �ػ����Ĳ��ɱ�
# Q     ��׮��������ص�׼������������µĸ��Ӻ���
# l     ׮��
# r     �������׮�����ߵ�ˮƽ����
# h     ���
# Es    ѹ��ģ��
# v     ���ɱ�
#׮����   {num:[x,y,a,b,Q,l,d,[(h,Es,v),...]],...}

def stiffness(num):
    pile_dict_all = load_paramenter()
    pile_dict = get_list(num,pile_dict_all)
    # num_list = pile_dict.keys()

    #  ȥ��׮�����ϲ���--------------->δ���

    l = pile_dict[num][3]            #׮��
    soil_list = pile_dict[num][5]      #��Ӧ���׮����

    z = l   #���
    sum_s = 0   #����
    for i in soil_list:      #���������

        # �������
        h = i[0]
        Es = i[1]
        v = i[2]

        #����h_list �����ֲ��б�
        thickness = 2  # �ֲ���-------���޸�
        if isinstance(h/thickness,int):
            soil_list_i_size = h // thickness       #�ֲ���
            h_list = soil_list_i_size*[thickness]
        else:
            soil_list_i_size = h//thickness+1
            h_last = h - (thickness*soil_list_i_size-1)        #���һ����
            h_list = soil_list_i_size * [thickness]+[h_last]

        for h in h_list:          #��thickness�ֲ����

            stress = 0   #����Ӧ��ֵ
            for k in pile_dict:

                a = pile_dict[k][0]  # ׮������ϵ��
                b = pile_dict[k][1]  # ��׮����ȷֲ�����ϵ��
                Q = pile_dict[k][2]  # ��׮��������ص�׼������������µĸ��Ӻ���
                l = pile_dict[k][3]  # ����
                r = pile_dict[k][6]  #����

                #���㲢�ۼӸ���Ӧ��ֵ
                m = mindlin(a, b, v, Q, l, r, z)
                stress += m[0] + m[1]
                # print(a, b, v, Q, l, r, z)
                # print(m[0] , m[1])
                # print(stress)


            sum_s += stress*h/Es   #�ۼƳ���ֵ
            z += h    #�ۼ����ֵ

    Q = pile_dict[num][2]
    E = Q/sum_s*1000
    return E


#����
# print(stiffness(200))
