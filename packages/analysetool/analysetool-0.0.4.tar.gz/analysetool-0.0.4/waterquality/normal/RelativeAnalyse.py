# 相关性分析
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import mpl
mpl.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"]=False


class RelativeAnalyse():

    def __init__(self):
        pass

    def relativeAnalyseByCondition(self,df,item_name="", mode="lt", first_val=None, second_val=None,output_img_path=""):
        df = selectDataByCondition(df,item_name=item_name,mode=mode,first_val=first_val,second_val=second_val)
        self.relativeAnalyseByOriginData(df,output_img_path=output_img_path)

    def relativeAnalyseByOriginData(self,df,output_img_path=""):
        df = clean(df)
        self.relativeAnalyse(df,output_img_path=output_img_path)

    # 定义相关性分析函数
    def relativeAnalyse(self,df, show_img=True, output_img_path=""):
        corr = df.corr()
        if show_img:
            colormap = plt.cm.RdBu
            plt.figure(figsize=(16, 4))
            fig  = sns.heatmap(corr, annot=True, cmap=colormap, vmin=-1, vmax=1)
            plt.show()
            if output_img_path != "" :
                heatmap = fig.get_figure()
                heatmap.savefig(output_img_path, dpi=400)

        return corr
