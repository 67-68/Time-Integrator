import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
import matplotlib.pyplot as plt
from scipy.optimize import brentq, minimize_scalar

# --- 1. 字体设置 ---
try:
    plt.rcParams['font.sans-serif'] = ['STHeiti']
except:
    print("STHeiti字体未找到，请尝试替换为系统支持的中文字体。")
plt.rcParams['axes.unicode_minus'] = False

# --- 2. 统一起点终点 ---
X_START, X_END = 0.0, 2.0
Y_END = 1.0
mu_values = np.arange(0.0, 0.51, 0.05)

# --- 3. 微分方程和求解函数 ---
def ode_friction(x, p, mu):
    if abs(p) < 1e-9:
        return 0.0
    return -2 * mu * p / (1 + p**2)

def solve_friction_curve(mu, x0, xf, p0, num_points=200):
    sol_p = solve_ivp(
        lambda x, p: ode_friction(x, p, mu),
        [x0, xf],
        [p0],
        method='RK45',
        dense_output=True,
        rtol=1e-6,
        atol=1e-9
    )
    x = np.linspace(x0, xf, num_points)
    p = sol_p.sol(x)[0]
    y = cumulative_trapezoid(p, x, initial=0)
    return x, y, p

# --- 4. 修复的摆线函数 ---
def brachistochrone_curve(x_target, y_target, num_points=200):
    """
    不解方程，直接用参数缩放把摆线拉到终点 (x_target, y_target)
    """
    # 先做一条“单位摆线”
    theta = np.linspace(0, np.pi, num_points)
    x_unit = theta - np.sin(theta)
    y_unit = 1 - np.cos(theta)

    # 缩放让它经过目标终点
    scale = x_target / x_unit[-1]
    x = x_unit * scale
    y = y_unit * scale

    # 如果竖直方向没到，再整体竖直缩放
    y *= y_target / y[-1]

    return x, y

# --- 5. 对齐终点并计算时间 ---
def scale_to_target(x, y, p, Xf, Yf):
    scale_x = Xf / (x[-1] + 1e-12)
    x_scaled = x * scale_x
    p_scaled = p * scale_x
    y_scaled = y * (Yf / (y[-1] + 1e-12))
    return x_scaled, y_scaled, p_scaled

def compute_time(x, y, p, mu, g=9.81):
    ds = np.sqrt(1 + p**2) * np.gradient(x)
    cos_theta = 1.0 / np.sqrt(1 + p**2)
    sin_theta = p / np.sqrt(1 + p**2)
    
    v = np.zeros_like(x)
    v[0] = 1e-6
    for i in range(1, len(x)):
        dv = g * (sin_theta[i] - mu * cos_theta[i]) * ds[i] / v[i-1]
        v[i] = v[i-1] + dv
        if v[i] <= 0:
            return np.inf
    return np.sum(ds / v)

# --- 6. 寻找最优初始斜率 ---
def find_optimal_p0(mu, Xf, Yf, p0_min=0.1, p0_max=10.0):
    def objective(p0):
        x, y, p = solve_friction_curve(mu, 0, 1, p0)
        x_scaled, y_scaled, p_scaled = scale_to_target(x, y, p, Xf, Yf)
        return compute_time(x_scaled, y_scaled, p_scaled, mu)
    
    res = minimize_scalar(objective, bounds=(p0_min, p0_max), method='bounded')
    return res.x, objective(res.x)

# --- 7. 绘图 ---
def plot_unified_curves():
    plt.figure(figsize=(12, 9))
    
    # 绘制摆线
    x_brach, y_brach = brachistochrone_curve(X_END, Y_END)
    plt.plot(x_brach, y_brach, 'k--', linewidth=2, label='无摩擦（经典摆线）')
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(mu_values)))
    optimal_p0s = []
    
    for i, mu in enumerate(mu_values):
        if mu == 0:
            optimal_p0s.append(None)
            continue
            
        p0_opt, _ = find_optimal_p0(mu, X_END, Y_END)
        optimal_p0s.append(p0_opt)
        
        x, y, p = solve_friction_curve(mu, 0, 1, p0_opt)
        x_scaled, y_scaled, p_scaled = scale_to_target(x, y, p, X_END, Y_END)
        
        label_text = f'$\\mu = {mu:.2f}$, $p_0^* = {p0_opt:.2f}$'
        plt.plot(x_scaled, y_scaled, color=colors[i], label=label_text)
    
    # 直线
    plt.plot([X_START, X_END], [0, Y_END], 'r:', label='直线路径')
    
    plt.xlabel('水平距离 x')
    plt.ylabel('竖直距离 y（向下为正）')
    plt.title('统一起点和终点的最优下滑曲线')
    plt.legend(title='参数')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    plot_unified_curves()