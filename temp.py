import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['STHeiti']  # 指定默认字体为 Mac 自带的“黑体-简”
plt.rcParams['axes.unicode_minus'] = False     # 解决保存图像是负号'-'显示为方块的问题

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# --- 1. 物理参数设定 ---
g = 9.81       # 重力加速度 (m/s²)
mu = 0.1       # 动摩擦系数
x_start, y_start = 0.0, 0.0  # 起点
x_end, y_end = 10.0, -5.0   # 终点

# --- 核心修正 4.0：回归最可靠的牛顿定律模型 ---
def ode_system(phi, state, mu, g):
    """
    基于牛顿第二定律的、最可靠的微分方程组。
    phi 是切线与竖直向下方向的夹角。
    state = [s, v]  <- 我们积分路程s和速度v
    """
    s, v = state
    
    # 避免速度为0导致除法错误
    if v <= 1e-9:
        v = 1e-9

    sin_phi = np.sin(phi)
    cos_phi = np.cos(phi)
    
    # 从 F=ma 推导出的核心微分方程
    # ds/dφ = v² / (g * (sin(φ) - μ*cos(φ)))
    ds_dphi = v**2 / (g * (sin_phi - mu * cos_phi))
    
    # dv/dφ = v / 2 * [d(v²)/ds] * (ds/dφ)
    # d(v²)/ds = 2g * (cos(φ) + μ*sin(φ))
    dv_dphi = v * (cos_phi + mu * sin_phi) / (sin_phi - mu * cos_phi)
    
    return np.array([ds_dphi, dv_dphi])

def simulate(phi_end, phi_initial=1e-6):
    """
    使用新的ODE模型进行模拟，并从s和v重构x和y。
    """
    # 初始状态: [s, v]
    v_initial = 1e-6 # 一个极小的初始速度
    initial_state = [0.0, v_initial] # 路程从0开始
    
    phi_span = [phi_initial, phi_end]
    
    sol = solve_ivp(
        fun=ode_system,
        t_span=phi_span,
        y0=initial_state,
        args=(mu, g),
        dense_output=True,
        method='RK45',
        rtol=1e-6, atol=1e-9
    )
    
    if not sol.success or not sol.y.size or np.any(np.isnan(sol.y)):
        return None, None, None

    # 从解中获取 s(φ) 和 v(φ)
    phi_eval = np.linspace(phi_span[0], phi_span[1], 300)
    s_of_phi, v_of_phi = sol.sol(phi_eval)
    
    # --- 关键步骤：从 s(φ) 重构 x(φ) 和 y(φ) ---
    # 因为 dx = ds * sin(φ) 和 dy = ds * cos(φ)
    # 所以 x(φ) = ∫ sin(φ) ds = ∫ sin(φ) * (ds/dφ) dφ
    #     y(φ) = ∫ cos(φ) ds = ∫ cos(φ) * (ds/dφ) dφ
    
    # 从我们的ODE解中，我们有 ds/dφ
    ds_dphi_vals = v_of_phi**2 / (g * (np.sin(phi_eval) - mu * np.cos(phi_eval)))
    
    # 使用 scipy.integrate.cumulative_trapezoid 进行数值积分来重构x和y
    from scipy.integrate import cumulative_trapezoid
    
    integrand_x = np.sin(phi_eval) * ds_dphi_vals
    integrand_y = np.cos(phi_eval) * ds_dphi_vals
    
    xs = cumulative_trapezoid(integrand_x, phi_eval, initial=0)
    ys = cumulative_trapezoid(integrand_y, phi_eval, initial=0)
    
    return xs, ys, ys[-1]

# --- 打靶法和侦察函数基本不变，只需适配新的simulate返回值 ---
def find_optimal_path():
    def error_function(phi_end):
        _, _, final_y = simulate(phi_end)
        if final_y is None:
            return 1e10
        return final_y - abs(y_end)

    try:
        search_interval = [mu, np.pi - 0.01] # 初始角度必须大于 arctan(mu)
        optimal_phi_end = brentq(error_function, search_interval[0], search_interval[1])
    except (ValueError, RuntimeError) as e:
        print(f"求根失败: {e}")
        print("请运行侦察模式并调整搜索区间。")
        return None, None, None

    xs, ys, _ = simulate(optimal_phi_end)
    return xs, -ys, optimal_phi_end

def investigate_phi_range():
    print("--- 启动侦察模式 (v4) ---")
    print(f"目标 y = {abs(y_end):.2f}")
    # 我们需要测试一个更合理的phi范围
    # 物体能开始下滑的最小角度是 arctan(μ)
    min_phi = np.arctan(mu)
    print(f"理论最小启动角 (arctan(μ)): {min_phi:.4f} rad")
    
    test_phis = np.linspace(min_phi + 0.1, np.pi - 0.01, 10)
    
    for phi in test_phis:
        _, _, final_y = simulate(phi)
        if final_y is not None:
            error = final_y - abs(y_end)
            print(f"当 phi_end = {phi:.4f} rad (~{np.rad2deg(phi):.2f}°), 模拟终点 y = {final_y:.4f}, 误差 = {error:.4f}")
        else:
            print(f"当 phi_end = {phi:.4f}, 模拟失败。")
    print("--- 侦察结束 ---")

# ... (后续的调用和绘图代码保持不变) ...

# 在调用主函数前，先运行侦察
investigate_phi_range()

# --- 4. 打靶法重构 ---
# 我们不再猜测初始斜率，而是猜测能够到达目标 y_end 的那个“最终角度” phi_end
def find_optimal_path():
    """
    使用打靶法（结合求根算法）寻找能精确到达终点的最优路径。
    """
    
    # 目标函数：我们希望找到一个 phi_end，使得模拟轨迹的终点 y 值正好是 y_end
    def error_function(phi_end):
        _, ys, _, _, _ = simulate(phi_end)
        if ys is None: # 模拟失败
            return 1e10 # 返回一个巨大的误差
        # 我们需要找到一个能让 y(phi_end) - y_target = 0 的 phi_end
        # 注意 y 是负的
        return ys[-1] - y_end

    # 使用一个高效且稳定的求根算法 (Brent's method) 来寻找最优的 phi_end
    # 我们需要提供一个包含根的区间，例如 [0.1, pi/2]
    try:
        # brentq 会在这个区间内寻找使 error_function 为 0 的 phi_end
        optimal_phi_end = brentq(error_function, 0.1, np.pi/2 - 0.01)
    except ValueError:
        print("求根失败，可能需要调整初始猜测区间。")
        return None, None, None, None

    # 使用找到的最优 phi_end 进行最后一次模拟，得到完整路径
    xs, ys, ts, final_x, total_time = simulate(optimal_phi_end)
    
    # 我们的打靶目标是 y_end，但最终的 x 坐标不一定正好是 x_end
    # 这是带摩擦力问题的固有特性：最速路径不一定能精确连接任意两点
    # 我们的解是最速到达 y = y_end 这条水平线的最优路径
    
    return xs, ys, total_time, final_x

# --- 5. 执行与绘图 ---
xs, ys, total_time, final_x = find_optimal_path()

if xs is not None:
    # 绘制无摩擦力的最速降线（摆线）作为对比
    # 找到能穿过 (x_end, y_end) 的摆线半径 r
    def cycloid_error(r):
        theta_end = 2 * np.arccos(1 - abs(y_end) / (2*r))
        return r * (theta_end - np.sin(theta_end)) - x_end
    
    try:
        r_cycloid = brentq(cycloid_error, abs(y_end)/2, 10)
        theta = np.linspace(0, 2 * np.arccos(1 - abs(y_end) / (2*r_cycloid)), 200)
        x_cycloid = r_cycloid * (theta - np.sin(theta))
        y_cycloid = -r_cycloid * (1 - np.cos(theta)) # y向下为正，所以加负号
        plt.plot(x_cycloid, y_cycloid, 'g--', label='无摩擦最速降线 (摆线)')
    except ValueError:
        print("无法计算无摩擦摆线路径。")


    plt.figure(figsize=(10, 7))
    plt.plot(xs, ys, 'b-', linewidth=2, label=f'带摩擦最速降线 (μ={mu})')
    plt.plot([x_start, x_end], [y_start, y_end], 'r--', label='直线路径')
    if 'y_cycloid' in locals():
        plt.plot(x_cycloid, y_cycloid, 'g-.', label='无摩擦最速降线 (摆线)', alpha=0.7)
    
    plt.scatter([x_start, xs[-1]], [y_start, ys[-1]], c='b', s=50, zorder=5)
    plt.scatter([x_end], [y_end], c='r', s=100, marker='*', label='目标终点 (y=-5)', zorder=5)
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('带摩擦力的最速降线 (Brachistochrone with Friction)')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"模拟完成!")
    print(f"总用时: {total_time:.4f} s")
    print(f"路径在 y={y_end} 处的 x 坐标为: {final_x:.4f} m (目标是 {x_end} m)")