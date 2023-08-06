import numpy as np

def get_intervals(x:np.ndarray, y:np.ndarray, level:float, delta:float=0.0001):
    from scipy.interpolate import interp1d
    func_interp = interp1d(x, y)
    x_interp = np.arange(min(x), max(x), delta)
    y_interp = func_interp(x_interp)

    asign = np.sign(y_interp - level)
    sign_change   = (np.roll(asign, 1) - asign) != 0
    intersections = x_interp[sign_change]
    sign_slope    = asign[sign_change]
    # no intersections
    if len(intersections) == 0:
        return []
    if len(intersections) == 1:
        if sign_slope[0] == -1:
            return np.array([[intersections[0], np.inf]])
        else:
            return np.array([[-np.inf, intersections[0]]])
    else:
        if sign_slope[0] == 1:
            intersections = np.insert(intersections, 0, -np.inf)
        if sign_slope[-1] == -1:
            intersections = np.insert(intersections, intersections.shape[0], np.inf)
        if len(intersections) & 1:
            raise RuntimeError("number of intersections can not be odd")
        n_pairs = len(intersections) // 2
        return intersections.reshape((n_pairs, 2))
    
def get_regular_meshgrid(*xi, n):
    reg_xi = [np.linspace(np.min(x), np.max(x), n) for x in xi]
    return np.meshgrid(*reg_xi)
    
def get_x_intersections(x1, y1, x2, y2):
    """Get intersections of two curves
    """
    interp_y1 = np.interp(x2, x1, y1) 

    diff = interp_y1 - y2 
    # determines what index intersection points are at 
    idx = np.argwhere(np.diff(np.sign(diff))).flatten()

    #linear interpolation to get exact intercepts: x = x1 + (x2-x1)/(y2-y1) * (y-y1)
    #y = 0 -> x = x1 - (x2-x1)/(y2-y1) * y1
    intersections = [x2[i] - (x2[i + 1] - x2[i])/(diff[i + 1] - diff[i]) * diff[i] for i in idx]
    return intersections