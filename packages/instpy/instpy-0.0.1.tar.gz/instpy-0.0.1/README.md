# **Instpy - Inferencial Stadistics Python**

<div align="center">
  <img src="./2.png"><br>
</div>

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DAVFoundation/captain-n3m0/blob/master/LICENSE)

# What is Instpy?

**instpy** is a stadistic library which permit you analyze measures obtaining main stadistical results
like

- `Histograms`
- `Qqplots`
- `Levene` test
- `Shapiro-Wilk` test
- `Parametric` or `Non parametric` test.  
  With this library you can test multiple or single measures, check if data verify normality condition or not and test measures against stadistic tests.
  Instpy has class where you can instance an object with following attributes:

```python
#Creating an InferencialStats object
InferencialStats(measures,alpha,is_paired,mean)
```

    measures: list lists of data (int or float)
    alpha (Optional): Significance level (float) E.g: 0.05 or 0.01
    is_paired (Optional) : bool flag to declare your measures as paired or non paired data
    mean (Optional): Scalar value to test against single measure

# Methods

The main method of this library.

## inferencial_statistics()

It executes an study about its attributes following next workflow

- ¿Single or multiple measures?
- Obtain `[Histogram , Qqplot , Shapiro-Wilk test results]` of every measure
- Perform `Levene Test`
- Perform `Parametric` or `Non-parametric` test depending on whether measures
  follow  
  **normal distribution** or **non normal distribution**

If you want to get _some additional features_ about your analysis you can try with
these methods

## crit_diff

Display a graphical analisys comapring critical differences from each measures

```
InferencialStats.crit_diff()
```

## show_hists

Plot a `plotly.graph_object.Figure` with all measure histograms

```
InferencialStats.show_hists();
```

## show_qqplots

Plot a `plotly.graph_object.Figure` with all measure qqplots

```
InferencialStats.show_qqplots();
```

## get_swtests

Return `Pana.DataFrame` with Shapiro-Wilk test results confirming if they follow or not a normal distribution

```
InferencialStats.get_swtests();
```

---

One method that is not vinculate with an InferencialStats object but library `Instpy`

## get_ranks

Get ranks of input measures

```
InferencialStats.get_ranks(measures);
```

---

# Installation

```sh
#With pip
pip install instpy
```

# Example

```python
import instpy
#Lets create some measures such as normal or uniform data distribution
x = np.random.normal(size=100).tolist()
y = np.random.normal(size=100).tolist()
t = np.random.normal(size=100).tolist()
z = np.random.normal(size=100).tolist()
#---------------------------------------------------------------------
xx = np.random.normal(size=100).tolist()
yx = np.random.normal(size=104).tolist()
tx = np.random.normal(size=110).tolist()
zx = np.random.normal(size=108).tolist()
#---------------------------------------------------------------------
```

## Single measure case

```python
#Create measure parameter
## Single data -------------
single_measure=[x]

res=InferecialStats(single_measure,is_paired=True,mean=80)
#Now lets analyze measure
res.inferencial_statistics()

#In this case it will only one plot
res.show_hists()
res.show_qqplots()
print(res.get_swtests())
print(res.get_t_res())
```

## Multiple measure case

Normal measures

```python
## Multiple data
data_measure=[x,y,z,t]

res=InferecialStats(data_measure,is_paired=True,alpha=0.05)
res.inferencial_statistics()
#-------Results-------
# [x]-->Histograms
# [x]-->Qqplot
# [x]-->Shapiro-Wilk test
# [x]-->Levene Test
# [x]-->Normality Condition
# [x]-->Parametric Test
#      |
#      |- One - Way ANOVA Repeated Measures
# [ ]-->Non Parametric Test
```

Non normal measures and unpaired

```python
## Multiple data

data_measure=[xx,yx,zx,tx]

res=InferecialStats(data_measure,is_paired=False,alpha=0.05)
res.inferencial_statistics()
#-------Results-------
# [x]-->Histograms
# [x]-->Qqplot
# [x]-->Shapiro-Wilk test
# [x]-->Levene Test
# [ ]-->Normality Condition
# [ ]-->Parametric Test
# [x]-->Non Parametric Test
#      |
#      |- Kruskal
```

# Author - Contact

Carlos Enrique - calollikito12000@gmail.com

# LICENSE

[MIT](LICENSE)
