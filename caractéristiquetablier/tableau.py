import numpy as np


coef_a1 = np.array(
  [ [0 ,0 ,0 ,0 ,0 , 0],
    [0 ,1 ,1 ,0.9 ,0.75 , 0.7],
    [0, 1, 0.9, 1, 1, 1, ],
    [0, 0.9, 0.8 , 1, 1, 1, ],
    ]

)



lv0_array = np.array([0,3.5, 3, 2.75])


coef_bc = np.array(
  [ 
    [0,0, 0, 0, 0, 0,],
    [0,1.2 ,1.1 ,0.95 , 0.8 , 0.7],
    [0,1, 1, 1, 1, 1,],
    [0,1,0.8, 1, 1, 1,],
    ]

)

coef_bt = np.array([0,1,0.9])


