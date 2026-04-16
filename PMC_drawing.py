# -*- coding: utf-8 -*-
# import sys
# import pandas as pd
# import numpy as np
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# from matplotlib import cm
# from mpl_toolkits.mplot3d import Axes3D
# from sklearn.preprocessing import MinMaxScaler
# import plotly.graph_objects as go
# from pathlib import Path
#
# # ================== 全局配置 ==================
# plt_style = {
#     'font.family': 'SimHei',
#     'axes.unicode_minus': False,
#     'figure.titlesize': 14,
#     'axes.labelsize': 10,
#     'figure.dpi': 150,
#     'savefig.bbox': 'tight'
# }
# plt.rcParams.update(plt_style)
#
#
# # ================== PMC曲面生成器 ==================
# class PMCSurfaceGenerator:
#     def __init__(self, features):
#         self.features = features
#         self.scaler = MinMaxScaler(feature_range=(0, 10))
#
#     def create_surface(self, ax, raw_values, title):
#         # 数据标准化
#         normalized = self.scaler.fit_transform(raw_values.reshape(-1, 1)).flatten()
#         matrix = normalized.reshape(3, 3)
#
#         # 创建网格
#         X, Y = np.meshgrid([0, 1, 2], [0, 1, 2])
#         Z = matrix
#
#         # 曲面绘制
#         surf = ax.plot_surface(X, Y, Z, cmap='Spectral_r',
#                                rstride=1, cstride=1,
#                                alpha=0.9, edgecolor='w',
#                                linewidth=0.5)
#
#         # 完整指标标注
#         for i in range(3):
#             for j in range(3):
#                 idx = 3 * i + j
#                 ax.text(i, j, Z[i, j] + 0.1,
#                         f"{self.features[idx]}\n({Z[i, j]:.1f})",
#                         ha='center', va='bottom',
#                         fontsize=7, color='#2F4F4F')
#
#         # 坐标轴设置
#         ax.set_xticks([0, 1, 2])
#         ax.set_xticklabels([f"{self.features[0:3][i]}\n(X{i + 1})" for i in range(3)],
#                            fontsize=7, rotation=5, linespacing=0.8)
#         ax.set_yticks([0, 1, 2])
#         ax.set_yticklabels([f"{self.features[3:6][i]}\n(X{i + 4})" for i in range(3)],
#                            fontsize=7, rotation=-12, linespacing=0.8)
#         ax.set_zlabel('效能维度\n(X7-X9)', fontsize=8)
#         ax.view_init(elev=28, azim=-135)
#         ax.set_title(title, fontsize=9, pad=3, color='#2F4F4F')
#         ax.dist = 10
#
#         return surf
#
#
# # ================== 可视化主函数 ==================
# def policy_visualization(excel_path):
#     # 数据准备
#     df = pd.read_excel(excel_path)
#     base_name = Path(excel_path).stem
#     output_dir = Path(excel_path).parent / f"{base_name}_可视化结果"
#     output_dir.mkdir(exist_ok=True)
#
#     provinces = df['省份'].tolist()
#     features = df.columns[1:10].tolist()
#
#     # ================== 紧凑雷达图 ==================
#     fig_radar, axes = plt.subplots(2, 2, figsize=(14, 10),
#                                    subplot_kw=dict(polar=True),
#                                    gridspec_kw={'hspace': 0.15, 'wspace': 0.1})
#     fig_radar.suptitle("省级政策指标雷达对比", y=0.98, fontsize=12)
#
#     angles = np.linspace(0, 2 * np.pi, 9, endpoint=False)
#     angles = np.append(angles, angles[0])
#
#     for ax, province in zip(axes.flat, provinces):
#         values = df.loc[df['省份'] == province, features].values.flatten().tolist()
#         values.append(values[0])
#
#         color = plt.cm.tab20(provinces.index(province))
#         ax.plot(angles, values, color=color, linewidth=1.2)
#         ax.fill(angles, values, color=color, alpha=0.15)
#         ax.set_xticks(angles[:-1])
#         ax.set_xticklabels([f"{feat[:6]}\n(X{i + 1})" for i, feat in enumerate(features)],
#                            fontsize=6, color='#4B4B4B')
#         ax.set_title(province, pad=6, fontsize=8, color='#2F4F4F')
#         ax.grid(color='#D3D3D3', linestyle=':', alpha=0.7)
#
#     plt.savefig(output_dir / f"{base_name}_雷达图对比.png", dpi=300)
#     plt.close()
#
#     # ================== 优化PMC曲面 ==================
#     generator = PMCSurfaceGenerator(features)
#     fig_3d = plt.figure(figsize=(14, 10))
#     fig_3d.suptitle("省级政策PMC曲面对比分析", y=0.98, fontsize=12)
#
#     plt.subplots_adjust(left=0.02, right=0.82,
#                         bottom=0.02, top=0.92,
#                         wspace=0.05, hspace=0.1)
#
#     for idx, province in enumerate(provinces, 1):
#         ax = fig_3d.add_subplot(2, 2, idx, projection='3d')
#         data = df.loc[df['省份'] == province, features].values.flatten()
#         surf = generator.create_surface(ax, data, province)
#
#         if idx == 1:
#             cax = fig_3d.add_axes([0.85, 0.15, 0.02, 0.7])
#             cb = fig_3d.colorbar(surf, cax=cax)
#             cb.ax.tick_params(labelsize=7)
#             cb.set_label('政策效能指数', fontsize=8)
#
#     plt.savefig(output_dir / f"{base_name}_PMC曲面图对比.png", dpi=300)
#     plt.close()
#
#     # ================== 高级桑基图 ==================
#     node_labels = [f"{feat[:8]}\n(X{i + 1})" for i, feat in enumerate(features)] + provinces
#     color_palette = mpl.colormaps['Set2'].resampled(12)  # 修正颜色映射方法
#
#     fig = go.Figure(go.Sankey(
#         arrangement="snap",
#         node=dict(
#             pad=15,
#             thickness=25,
#             line=dict(width=0.5, color='#808080'),
#             label=node_labels,
#             color=[mpl.colors.to_hex(color_palette(i % 12)) for i in range(len(node_labels))],
#             hovertemplate="<b>%{label}</b><br>流量值: %{value}<extra></extra>"
#         ),
#         link=dict(
#             source=[i for i in range(9) for _ in range(4)],
#             target=[9 + i // 9 for i in range(36)],
#             value=df[features].values.flatten().tolist() * 4,
#             color=[mpl.colors.to_hex(color_palette(i % 12)) for i in range(36)],
#             hovertemplate="<b>来源:</b> %{source.label}<br><b>目标:</b> %{target.label}<br>数值: %{value}<extra></extra>"
#         )
#     ))
#
#     fig.update_layout(
#         title_text="政策指标桑基分析图",
#         title_font_size=14,
#         font=dict(size=10, color='#2F4F4F'),
#         height=800,
#         width=1200,
#         margin=dict(l=60, r=60, b=30, t=80),
#         plot_bgcolor='#F8F8FF',
#         paper_bgcolor='#FFFFFF'
#     )
#     fig.write_html(output_dir / f"{base_name}_桑基图.html")
#
#     print(f"🎯 可视化结果已保存至：{output_dir}")
#
#
# # ================== 执行入口 ==================
# if __name__ == "__main__":
#     excel_path = r'E:\phdresearch\caltransfer\data\area\四省综合评估报告6.xlsx'  # 修改为实际路径
#     policy_visualization(excel_path)
# r'E:\phdresearch\caltransfer\data\area\绘图\PMC_drawing.xlsx'
"""
2.0 豆包对比
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from plotly.graph_objects import Figure, Sankey
import plotly.io as pio

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 读取文件
file_path = r"E:\phdresearch\caltransfer\data\area\四省综合评估报告8.xlsx"
df = pd.read_excel(file_path)

# 提取省份、指标和 PMC 总指标
provinces = df['省份'].tolist()
indicators = [f"政策性质X1_分位数", "效力级别X2_分位数", "作用领域X3_分位数",
              "政策工具X4_分位数", "政策客体X5_分位数", "政策内容X6_分位数",
              "算力政策保障X7_分位数", "政策协同性X8_分位数", "政策功能X9_分位数"]
pmc_total = df['省级PMC总指标'].tolist()

# 提取指标数据
indicator_data = df[indicators].values

# （1）绘制雷达图
labels = indicators
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# 定义颜色列表
colors = list(mcolors.TABLEAU_COLORS.values())
# 定义线的样式列表
line_styles = ['-', '--', '-.', ':']

for i, province in enumerate(provinces):
    values = indicator_data[i].tolist()
    values += values[:1]
    ax.plot(angles, values, color=colors[i], linewidth=2, label=province, linestyle=line_styles[i])
    ax.fill(angles, values, color=colors[i], alpha=0.25)

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], labels, fontsize=8)
ax.set_rlabel_position(0)
plt.yticks([0.2, 0.4, 0.6, 0.8], color="grey", size=7)
plt.ylim(0, 1)
# 调大雷达图的图例
plt.legend(loc='upper right', bbox_to_anchor=(1.7, 1), fontsize=10)
plt.title("四省份各省级一级指标雷达图", fontsize=12)
# 保存雷达图
radar_path = file_path.rsplit('.', 1)[0] + '_雷达图.png'
plt.tight_layout()
plt.savefig(radar_path)
plt.close()

# （2）绘制各省分 PMC 曲面图
fig = plt.figure(figsize=(12, 12))
for i, province in enumerate(provinces):
    ax = fig.add_subplot(2, 2, i + 1, projection='3d')
    指标矩阵 = indicator_data[i].reshape(3, 3)
    x = np.arange(3)
    y = np.arange(3)
    X, Y = np.meshgrid(x, y)
    Z = 指标矩阵
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black', linewidth=0.5)  # 增加黑色边框以区分面

    # 标注各个一级指标以及对应数值，并动态调整文字位置以减少遮挡
    for xi in range(3):
        for yi in range(3):
            index = xi * 3 + yi
            # 计算相邻点的最大高度差，以此作为偏移量的参考
            max_diff = 0
            if xi > 0:
                max_diff = max(max_diff, abs(Z[xi, yi] - Z[xi - 1, yi]))
            if xi < 2:
                max_diff = max(max_diff, abs(Z[xi, yi] - Z[xi + 1, yi]))
            if yi > 0:
                max_diff = max(max_diff, abs(Z[xi, yi] - Z[xi, yi - 1]))
            if yi < 2:
                max_diff = max(max_diff, abs(Z[xi, yi] - Z[xi, yi + 1]))

            z_offset = 0.02 + 0.1 * max_diff  # 基础偏移量加上与相邻点高度差相关的偏移量
            ax.text(xi, yi, Z[xi, yi] + z_offset, f"{indicators[index]}: {Z[xi, yi]:.2f}",
                    color='black', fontsize=6, ha='center', va='center')

    ax.set_xlabel('指标维度1', fontsize=8)
    ax.set_ylabel('指标维度2', fontsize=8)
    ax.set_zlabel('指标值', fontsize=8)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['政策性质X1', '政策工具X4', '算力政策保障X7'], fontsize=6)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(['效力级别X2', '政策客体X5', '政策协同性X8'], fontsize=6)
    ax.set_title(f'{province} PMC 曲面图', fontsize=10)

# 调整 PMC 曲面图的颜色条位置和大小，避免与右侧竖轴遮挡
fig.subplots_adjust(right=0.85)
cax = fig.add_axes([0.9, 0.15, 0.03, 0.7])
fig.colorbar(surf, cax=cax, shrink=0.5, aspect=5)

# 手动调整子图参数，让四个省份的图件布局更紧密
plt.subplots_adjust(left=0.05, right=0.85, bottom=0.05, top=0.95, wspace=0.1, hspace=0.1)

# 保存 PMC 曲面图
pmc_surface_path = file_path.rsplit('.', 1)[0] + '_PMC曲面图.png'
plt.savefig(pmc_surface_path)
plt.close()

# （3）绘制桑基图
source = []
target = []
value = []
color = []
label = []

# 左侧一级指标标签
一级指标标签 = [f"政策性质X1", "效力级别X2", "作用领域X3",
                "政策工具X4", "政策客体X5", "政策内容X6",
                "算力政策保障X7", "政策协同性X8", "政策功能X9"]
label.extend(一级指标标签)

# 右侧 PMC 总指标标签
for province in provinces:
    label.append(f'{province} 省级PMC总指标')

# 定义更柔和的颜色组合
soft_colors = ['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f']

# 构建桑基图数据
for i, indicator in enumerate(一级指标标签):
    for j, province in enumerate(provinces):
        source.append(i)
        target.append(len(一级指标标签) + j)
        value.append(indicator_data[j][i])
        color.append(soft_colors[j])

# 创建桑基图
fig = Figure(data=[Sankey(
    node=dict(
        pad=5,  # 减小节点间距
        thickness=20,
        line=dict(color="black", width=0.5),
        label=label,
        color=soft_colors * len(一级指标标签) + soft_colors[:len(provinces)]
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=color,
        line=dict(color="black", width=0.5)
    ),
    arrangement='snap'  # 缩短输入值和输出值之间的距离
)])

fig.update_layout(title_text="四省份省级一级指标与省级PMC总指标桑基图", font_size=12)
# 保存桑基图为 HTML 文件
sankey_path = file_path.rsplit('.', 1)[0] + '_桑基图.html'
pio.write_html(fig, sankey_path)

print(f"雷达图已保存至: {radar_path}")
print(f"PMC 曲面图已保存至: {pmc_surface_path}")
print(f"桑基图已保存至: {sankey_path}")






