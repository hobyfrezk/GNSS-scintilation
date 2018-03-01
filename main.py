# Title:    Scintillation detection tool based on machine learning algorithms
# Author:   Group B     Yejia XU
#                       Qizhen LU
#                       Minghao Liu
#                       Chongshun Wang
#                       Ayub Yimer Endris
# Date:     11/3/2017


from MainFrame import *

from Dataset import Dataset
from Algorithm import Algorithm
from Evaluation import Evaluation
def test():
    # For test ---
    filename = 'dset_james_merged_satnum.csv'
    d = Dataset(filename)
    a = Algorithm()
    e = Evaluation(d,a)
    e.getCrossValScores()
    e.plot_PRN_Date(3)
    # End test ---
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = Mainframe()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()