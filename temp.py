import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
import math

# --- 1. 字体设置 (保持不变) ---
try:
    plt.rcParams['font.sans-serif'] = ['STHeiti']
    plt.rcParams['axes.unicode_minus'] = False
except:
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

# --- 2. 参数设置 ---
g = 9.8  # 重力加速度 (m/s²)
start_point = (0.0, 0.0)
end_point = (19.59, -13.06)
mu_fixed = 0.2  # *** 核心修改：直接指定摩擦系数 ***

x1, y1 = end_point

print("--- 设定参数 ---")
print(f"目标终点: ({x1}, {y1})")
print(f"固定摩擦系数 μ = {mu_fixed:.2f}")
print("-" * 20)

# --- 3. 参数方程和求解器函数 (保持不变) ---
def get_xy_coords(t, C, mu):
    """根据给定的参数 t, C, μ 计算 x 和 y 坐标 (y轴方向已修正)"""
    common_factor = C / (1 + mu**2) / 2
    x = common_factor * (1 - np.cos(t) - mu * np.sin(t))
    y_downward = common_factor * (np.sin(t) - mu * (1 - np.cos(t))) + mu * x
    return x, -y_downward

def find_parameters(t_final, target_x, target_y, mu):
    """目标函数，用于 scipy.optimize.root_scalar 寻找 t_final"""
    denominator_C = 1 - np.cos(t_final) - mu * np.sin(t_final)
    if abs(denominator_C) < 1e-9:
        return 1e6
    C = 2 * target_x * (1 + mu**2) / denominator_C
    _, calculated_y = get_xy_coords(t_final, C, mu)
    return calculated_y - target_y

def solve_for_curve(mu, target_x, target_y):
    """为给定的 μ 求解曲线参数 C 和 t_final，使用动态 bracket"""
    try:
        if mu > 0:
            t_start = 2 * math.atan(mu)
        else:
            t_start = 0
        bracket_low = t_start + 0.01
        bracket_high = 2 * math.pi - 0.01

        sol = root_scalar(
            f=find_parameters,
            args=(target_x, target_y, mu),
            bracket=[bracket_low, bracket_high],
            method='brentq'
        )
        if sol.converged:
            t_final = sol.root
            denominator_C = 1 - np.cos(t_final) - mu * np.sin(t_final)
            C_final = 2 * target_x * (1 + mu**2) / denominator_C
            return C_final, t_final
    except ValueError as e:
        print(f"错误：为 μ={mu:.4f} 求解失败。求解器未能找到有效的根。错误信息: {e}")
        return None, None
    return None, None

# --- 4. 计算并准备绘图数据 ---
# 4.1 计算 μ = 0.2 的曲线
print(f"正在为 μ = {mu_fixed:.2f} 求解曲线参数...")
C_solution, t_final_solution = solve_for_curve(mu_fixed, x1, y1)

v_final_calculated = 0.0
if C_solution is not None:
    print(f"求解成功: C = {C_solution:.4f}, t_final = {t_final_solution:.4f}")
    t_values_sol = np.linspace(0, t_final_solution, 500)
    x_sol, y_sol = get_xy_coords(t_values_sol, C_solution, mu_fixed)
    
    # *** 核心修改：根据 μ 计算终点速度 ***
    v_final_sq = 2 * g * (-y1 - mu_fixed * x1)
    if v_final_sq > 0:
        v_final_calculated = math.sqrt(v_final_sq)
        print(f"计算得出，当 μ={mu_fixed:.2f} 时，终点速度为: {v_final_calculated:.2f} m/s")
    else:
        print("警告：摩擦力过大，物体无法到达终点。")

# 4.2 计算无摩擦的最速降线作为对比 (可选，但建议保留)
print("\n正在计算无摩擦(μ=0)的最速降线用于对比...")
C_ref, t_final_ref = solve_for_curve(0.0, x1, y1)
if C_ref is not None:
    print(f"求解成功: C = {C_ref:.4f}, t_final = {t_final_ref:.4f}")
    t_values_ref = np.linspace(0, t_final_ref, 500)
    x_ref, y_ref = get_xy_coords(t_values_ref, C_ref, 0.0)

# --- 5. 绘图 ---
plt.figure(figsize=(12, 8))

# 绘制 μ = 0.2 的曲线
if 'x_sol' in locals():
    label_text = (f'固定摩擦系数曲线 (μ = {mu_fixed:.2f})\n'
                  f'计算出的终点速度 = {v_final_calculated:.2f} m/s')
    plt.plot(x_sol, y_sol, label=label_text, color='crimson', linewidth=3, zorder=5)
else:
    print("\n警告：未能生成目标曲线，将不会在图中显示。")

# 绘制无摩擦的参考曲线
if 'x_ref' in locals():
    plt.plot(x_ref, y_ref, label='最速降线 (μ = 0.0)\n无摩擦对比', 
             color='dodgerblue', linestyle='--', linewidth=2)

# 图表美化
plt.scatter(start_point[0], start_point[1], color='black', s=150, label='起点(0,0)', zorder=10)
plt.scatter(end_point[0], end_point[1], color='blue', s=150, label=f'终点({x1:.2f},{y1:.2f})', zorder=10)
plt.title(f'固定摩擦系数 μ = {mu_fixed:.2f} 的最速降线', fontsize=16, fontweight='bold')
plt.xlabel('水平位移 x (m)', fontsize=12)
plt.ylabel('竖直位移 y (m)', fontsize=12)
plt.legend(fontsize=11, frameon=True, shadow=True)
plt.grid(True, linestyle='--', alpha=0.6)
plt.axis('equal')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.tight_layout()

# 保存并显示图像
plt.savefig(f'brachistochrone_mu_{mu_fixed}.png', dpi=300)
plt.show()