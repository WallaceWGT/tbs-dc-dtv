function ChartDataFormat(chart_data) {
    /*
    * 功能：根据需要的图表形式, 将后端传送过来的数据结构进行解析，使数据格式符合图表的数据格式
    * chart_data: 后端数据格式{'type':1, 'title':[], data:[[1,], [2,], [3,]]}
    * type:表示图表样式,
    * title: 表示的是查询字段的标题一般来说
    * data:数据库查询的数据(一般为二维数组)
    *
    * */

    var data=[];
    var title=chart_data['title'];
    // 对传过来的的数据转换成一维数组是数据结构与之对应的都是时间字段[dt, 可分], [[20180101, 1], [2018, 2]]
    function OneDimensionalArray(chart_data) {
        var field = [];
        $.each(chart_data['data'], function (i, x) {
            field.push(x[0]);
            data.push(x[1]);
        });
    }
    // 对传递过来的数据转换成Object的数据结构 [可分, 未分, 已分], [[1, 2, 3], ]
    function ObjData(chart_data) {
        var title = chart_data["title"];
        $.each(title, function (i, x) {
            var dataElement={};
            $.each(chart_data['data'], function (j, y) {
                if (i===j){
                    dataElement['name'] = x;
                    dataElement['value'] = y[0];
                    data.push(dataElement);
                }
            })
        });
    }
    // 判断图形类型,根据给定的数据集，生成对应格式的数据
    switch (chart_data['chartType']) {
        case '1':   // 折线图 返回：title[20180101, 20181012, 20180103], data=[1, 2, 4]
            OneDimensionalArray(chart_data);
            break;
        case '2':   // 柱状图 返回：title[20180101, 20181012, 20180103], data=[1, 2, 4]
            console.log('daf')
            OneDimensionalArray(chart_data);
            break;
        case '3':   // 雷达图
            OneDimensionalArray(chart_data);
            break;
        case '4':   // 饼图 {'key': value, 'key2': value2}
            ObjData(chart_data);
            break;
        case '5':   // 地图 {'key': value, 'key2': value2}
            ObjData(chart_data);
            break;
        case '6':   // 漏斗图 {'key': value, 'key2': value2}
            ObjData(chart_data);
            break;
        case '7':   // 用于平行坐标系 [[1, 3, 3], [2, 3, 4], [1, 2, 4]]---->['已分', '未分', '可分']  使用的就是源数据
            data = chart_data['data'];
            break;
        case '8':   //  返回得到的数据格式   ['时间', 20180101, 20180102, 20180103, 20180104], [可分, 11, 12, 13, 14, 15], [未分, 12, 31, 33, 43, 23], [已分, 12, 3, 5, 6, 7, 6]
            $.each(title, function (i, x) {
                data.push(x);
                $.each(chart_data['data'], function (j, y) {
                    data.push(y[i])
                })
            });
    }


    return {"title": title, "data":data}
}
