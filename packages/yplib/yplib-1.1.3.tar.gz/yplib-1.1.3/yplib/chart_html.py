# 使用 echarts 的基本图表
def chart_html(option=''):
    s = '<!DOCTYPE html>' \
        '<html lang="zh-CN" style="height: 100%">' \
        '<head>' \
        '    <meta charset="utf-8">' \
        '</head>' \
        '<body style="height: 100%; margin: 0">' \
        '<div id="container" style="height: 100%"></div>' \
        '<script type="text/javascript" src="https://fastly.jsdelivr.net/npm/echarts@5.4.2/dist/echarts.min.js"></script>' \
        '<script type="text/javascript">' \
        '    var dom = document.getElementById("container");' \
        '    var myChart = echarts.init(dom, null, {' \
        '        renderer: "canvas",' \
        '        useDirtyRect: false,' \
        '    });' \
        '    var app = {};' \
        '    var option = -option-;' \
        '    if (option && typeof option === "object") {' \
        '        myChart.setOption(option);' \
        '    }' \
        '    window.addEventListener("resize", myChart.resize);' \
        '</script>' \
        '</body>' \
        '</html>' \
        ''
    return s.replace('-option-', option)


# 折线图的 html 模板代码
def line_stack_html():
    option = '{' \
             '    title: {' \
             '        text: "-chart_name-",' \
             '    },' \
             '    tooltip: {' \
             '        trigger: "axis",' \
             '    },' \
             '    dataZoom: [' \
             '        {' \
             '            show: true,' \
             '            realtime: true,' \
             '        },' \
             '        {' \
             '            type: "inside",' \
             '            realtime: true,' \
             '        },' \
             '    ],' \
             '    grid: {' \
             '        left: "30px",' \
             '        right: "40px",' \
             '        bottom: "80px",' \
             '        containLabel: true,' \
             '    },' \
             '    toolbox: {' \
             '        feature: {' \
             '            saveAsImage: {},' \
             '        },' \
             '    },' \
             '    yAxis: {' \
             '        type: "value",' \
             '    },' \
             '    xAxis: {' \
             '        type: "category",' \
             '        boundaryGap: false,' \
             '        data: -x_list-,' \
             '    },' \
             '    legend: {' \
             '        -legend-,' \
             '    },' \
             '    series: -series-,' \
             '}'
    return chart_html(option)


# 饼图的 html 模板代码
def pie_html():
    option = '{' \
             '  tooltip: {' \
             '    trigger: "item"' \
             '  },' \
             '  legend: {' \
             '    top: "5%",' \
             '    left: "center"' \
             '  },' \
             '  series: [' \
             '    {' \
             '      name: "Access From",' \
             '      type: "pie",' \
             '      radius: ["30%", "70%"],' \
             '      itemStyle: {' \
             '        borderRadius: 10,' \
             '        borderColor: "#fff",' \
             '        borderWidth: 1' \
             '      },' \
             '      emphasis: {' \
             '        label: {' \
             '          show: true,' \
             '          fontSize: 30,' \
             '          fontWeight: "bold"' \
             '        }' \
             '      },' \
             '      labelLine: {' \
             '        show: true' \
             '      },' \
             '      data: -data-' \
             '    }' \
             '  ]' \
             '}'
    return chart_html(option)


# 柱状的 html 模板代码
def bar_html():
    option = '{' \
             '  title: {' \
             '    text: "",' \
             '    left: 10' \
             '  },' \
             '  toolbox: {' \
             '    feature: {' \
             '      dataZoom: {' \
             '        yAxisIndex: false' \
             '      },' \
             '      saveAsImage: {' \
             '        pixelRatio: 2' \
             '      }' \
             '    }' \
             '  },' \
             '  tooltip: {' \
             '    trigger: "axis",' \
             '    axisPointer: {' \
             '      type: "shadow"' \
             '    }' \
             '  },' \
             '  grid: {' \
             '    bottom: 90' \
             '  },' \
             '  dataZoom: [' \
             '    {' \
             '      type: "inside"' \
             '    },' \
             '    {' \
             '      type: "slider"' \
             '    }' \
             '  ],' \
             '  xAxis: {' \
             '    data: -x_list-,' \
             '    silent: false,' \
             '    splitLine: {' \
             '      show: false' \
             '    },' \
             '    splitArea: {' \
             '      show: false' \
             '    }' \
             '  },' \
             '  yAxis: {' \
             '    splitArea: {' \
             '      show: false' \
             '    }' \
             '  },' \
             '  series: [' \
             '    {' \
             '      type: "bar",' \
             '      data: -y_list-,' \
             '      large: true' \
             '    }' \
             '  ]' \
             '}'
    return chart_html(option)
