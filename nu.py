import glob
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
import scipy.stats as sts
import math

def setdir(path):
    os.chdir(path)    

def load(name, sep=',', nrows=None):
    dfs = [pd.read_csv(file, index_col=False, sep=sep, nrows=nrows) for file in glob.glob("*.csv") if file.startswith(name + '.')]
    return dfs

def plot_separate(name, key, xkey=None, sep=',', nrows=None):
    dfs = load(name, sep, nrows)
    n_runs = len(dfs)
    print('%s: plotting %d runs' % (name, n_runs))
    
    for df in dfs:
        value = df[key]
        xx = range(len(value)) if xkey is None else df[xkey]
        plt.plot(xx, value, alpha=max(1/n_runs, 0.3))
        
    plt.xlabel('iterations' if xkey is None else xkey)
    plt.ylabel(key)

def plot_mean(name, key, xkey=None, sep=',', nrows=None):
    dfs = load(name, sep, nrows)
    n_runs = len(dfs)
    print('%s: aggregating %d runs' % (name, n_runs))
    cdf = pd.concat(dfs, sort=True).groupby(level=0)
    
    df = cdf.mean()
    value = df[key]
    xx = range(len(value)) if xkey is None else df[xkey]
    plt.plot(xx, value)
    
    plt.xlabel('iterations' if xkey is None else xkey)
    plt.ylabel(key)

def plot_student(name, key, conf=0.95, xkey=None, sep=',', nrows=None):
    dfs = load(name, sep, nrows)
    n_runs = len(dfs)
    print('%s: aggregating %d runs' % (name, n_runs))
    cdf = pd.concat(dfs, sort=True).groupby(level=0)
    
    df = cdf.mean()
    sdf = cdf.std().fillna(0)
    std = sdf[key]
    mean = df[key]
    xx = range(len(mean)) if xkey is None else df[xkey]
    plt.plot(xx, mean)
    
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="invalid value encountered in multiply")
        interval = sts.t.interval(conf, n_runs-1,loc=mean,scale=std/math.sqrt(n_runs))    
    plt.fill_between(xx, interval[0], interval[1], alpha=0.3)
    
    plt.xlabel('iterations' if xkey is None else xkey)
    plt.ylabel(key)
    
def compare_student(names, key, conf=0.95, xkey=None, sep=',', nrows=None):
    for name in names:
        plot_student(name, key, conf, xkey, sep, nrows)
    
    plt.legend(names)
    
def compare_separate(names, key, xkey=None, sep=',', nrows=None):
    for name in names:
        plot_separate(name, key, xkey, sep, nrows)