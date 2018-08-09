function init_echart() {

    <!--石斑鱼数量统计 echarts init-->

    var chartOneDom = document.getElementById("b-line");
    var chartOne = echarts.init(chartOneDom);
    chartOne.showLoading();
    $.get("/fishes/admin/getfishnum/").done(function (data) {
        chartOne.hideLoading();
        var data  = JSON.parse(data);
        chartOne.setOption({
        color: ['#4aa9e9'],
        title: {
            text: '石斑鱼数量统计',
            //subtext: '纯属虚构',
            x: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: function (params, ticket, callback) {
                return "数量：" + params[0].value + '<br>' + "品种：" + params[1].value;
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: data.pool_num,
            axisTick: {
                alignWithLabel: true
            },
        },
        series: [
            {
                name: '石斑鱼数量',
                type: 'bar',
                stack: '堆叠',
                barWidth: '20%',
                label: {
                    normal: {
                        show: true,
                        position: 'insideRight'
                    }
                },
                data: data.fish_num
            },
            {
                name: '石斑鱼品种',
                type: 'bar',
                stack: '堆叠',
                barWidth: '20%',
                label: {
                    normal: {
                        show: true,
                        position: 'insideRight'
                    }
                },
                data: data.variety
            },
        ]
    })
    });

    // var chartOneOption = {
    //     color: ['#4aa9e9'],
    //     title: {
    //         text: '石斑鱼数量统计',
    //         //subtext: '纯属虚构',
    //         x: 'center'
    //     },
    //     tooltip: {
    //         trigger: 'axis',
    //         axisPointer: {            // 坐标轴指示器，坐标轴触发有效
    //             type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
    //         },
    //         formatter: function (params, ticket, callback) {
    //             return "数量：" + params[0].value + '<br>' + "品种：" + params[1].value;
    //         }
    //     },
    //     grid: {
    //         left: '3%',
    //         right: '4%',
    //         bottom: '3%',
    //         containLabel: true
    //     },
    //     xAxis: {
    //         type: 'value'
    //     },
    //     yAxis: {
    //         type: 'category',
    //         data: ['鱼池1号', '鱼池2号', '鱼池3号'],
    //         axisTick: {
    //             alignWithLabel: true
    //         },
    //     },
    //     series: [
    //         {
    //             name: '直接访问',
    //             type: 'bar',
    //             stack: '堆叠',
    //             barWidth: '20%',
    //             label: {
    //                 normal: {
    //                     show: true,
    //                     position: 'insideRight'
    //                 }
    //             },
    //             data: [320, 202, 30]
    //         },
    //         {
    //             name: '邮件营销',
    //             type: 'bar',
    //             stack: '堆叠',
    //             barWidth: '20%',
    //             label: {
    //                 normal: {
    //                     show: true,
    //                     position: 'insideRight'
    //                 }
    //             },
    //             data: ['品种1', '品种2', '品种3']
    //         },
    //     ]
    // };
    //
    // if (chartOneOption && typeof chartOneOption === "object") {
    //     chartOne.setOption(chartOneOption, true);
    // }


    <!--品种分析 echarts init-->

    var chartTwoDom = document.getElementById("b-area");
    var chartTwo = echarts.init(chartTwoDom);

    chartTwo.showLoading();
    $.get("/fishes/admin/getvarityfishnum/").done(function (data) {
        chartTwo.hideLoading();
        //console.log(data);
        var data = JSON.parse(data);
        chartTwo.setOption({
            title: {
                text: '石斑鱼品种分析',
                //subtext: '纯属虚构',
                x: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>数量 : {c} <br/>占比：{d}%"
            },
            legend: {
                orient: 'vertical',
                left: 'right',
                data: data.variety
            },
            series: [
                {
                    name: '品种数量统计',
                    type: 'pie',
                    radius: ['20%', '65%'],
                    center: ['50%', '60%'],
                    roseType: 'radius',
                    label: {
                        normal: {
                            position: 'inner'
                        }
                    },
                    data: data.seriesData,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        })
    });
//     option = {
//     title : {
//         text: '石斑鱼品种分析',
//         //subtext: '纯属虚构',
//         x:'center'
//     },
//     tooltip : {
//         trigger: 'item',
//         formatter: "{a} <br/>数量 : {c} <br/>占比：{d}%"
//     },
//     legend: {
//         orient: 'vertical',
//         left: 'right',
//         data: ['品种1','品种2','品种3']
//     },
//     series : [
//         {
//             name: '品种数量统计',
//             type: 'pie',
//             radius : ['20%', '65%'],
//             center: ['50%', '60%'],
//             roseType : 'radius',
//             label: {
//                 normal: {
//                     position: 'inner'
//                 }
//             },
//             data:[
//
//                 {value:35, name:'品种1'},
//                 {value:30, name:'品种2'},
//                 {value:23, name:'品种3'},
//
//             ],
//             itemStyle: {
//                 emphasis: {
//                     shadowBlur: 10,
//                     shadowOffsetX: 0,
//                     shadowColor: 'rgba(0, 0, 0, 0.5)'
//                 }
//             }
//         }
//     ]
// };
//
//
//     if (option && typeof option === "object") {
//         myChart.setOption(option, false);
//     }


    <!--Rainfall and Evaporation echarts init-->

    var chartThreeDom = document.getElementById("rainfall");
    var chartThree = echarts.init(chartThreeDom);

    $.get("/fishes/admin/getprocesshnum/").done(function (data) {
        var data = JSON.parse(data);
        console.log(data);
        console.log(data.date);
        console.log(data.data);
        chartThree.setOption({
            color: ['#4aa9e9'],
            title: {
                text: '生产统计',
                //subtext: '纯属虚构',
                x: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            dataZoom: [
                {
                    type: 'slider',
                    show: true,
                    xAxisIndex: [0],
                    startValue: data.start,
                    endValue: data.end
                },
                {
                    type: 'inside',
                    xAxisIndex: [0],
                    startValue: data.start,
                    endValue: data.end
                },
            ],
            xAxis: {
                type: 'category',
                data: data.date,
                axisTick: {
                    alignWithLabel: true
                },

            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: data.data,
                type: 'line'
            }]
        });
    });

//     var app = {};
//     option = null;
//     option =  {
//     color: ['#4aa9e9'],
//     title: {
//             text: '生产统计',
//             //subtext: '纯属虚构',
//             x: 'center'
//     },
//     tooltip:{
//         trigger: 'axis',
//         axisPointer: {
//             type: 'cross'
//         }
//     },
//     dataZoom: [
//         {
//             type: 'slider',
//             show: true,
//             xAxisIndex: [0],
//             startValue: '2018-08-03',
//             endValue: '2018-08-06'
//         },
//         {
//             type: 'inside',
//             xAxisIndex: [0],
//             startValue: '2018-08-03',
//             endValue: '2018-08-06'
//         },
//     ],
//     xAxis: {
//         type: 'category',
//         data: ['2018-08-01', '2018-08-02', '2018-08-03', '2018-08-04', '2018-08-05', '2018-08-06', '2018-08-07'],
//         axisTick: {
//                 alignWithLabel: true
//         },
//
//     },
//     yAxis: {
//         type: 'value'
//     },
//     series: [{
//         data: [320, 432, 91, 434, 290, 630, 120],
//         type: 'line'
//     }]
// };
//
//     if (option && typeof option === "object") {
//         chartThree.setOption(option, false);
//     }

    /**
     * Resize chart on window resize
     * @return {void}
     */
    window.onresize = function() {
        chartOne.resize();
        chartTwo.resize();
        chartThree.resize();
    };
};

$(document).ready(init_echart());
