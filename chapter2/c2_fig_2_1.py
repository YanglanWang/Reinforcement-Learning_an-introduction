import numpy as np
import matplotlib.pyplot as plt
fig,axes=plt.subplots(1,1)
axes.violinplot(np.random.randn(100,10)+np.random.randn(10),showmeans = True)
plt.savefig('c2_fig_2_1.png')
plt.show()
