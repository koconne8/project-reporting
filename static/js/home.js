// today's date
var today = new Date();

// expected hours
var expected = 0;

function GetOverview()
{
	$.ajax({
		url: '../get_entries',
		data: {month: today.getMonth() + 1, year: today.getFullYear(), order: 'date', by: 'asc'},
		dataType: 'json',
		success: function(data){
			// billable hours
			$("#billable_hours").html(data.total);
			// non-billable
			$('#support_hours').html(data.support);
			// total
			$('#total_hours').html(parseFloat(data.support) + parseFloat(data.total));
			// expected
			$('#expected').html(data.weekdays);

			expected = data.billable;

			SetupExpected(data.entries);
		
		},
		error: function(){
			alert("Failed to get hourly summary!");
		}
	});
}

function SetupExpected(data)
{
	var entries = new Array();
	var expected_list = new Array();
	var dates = new Array();

	var next_date = '';
	var current_sum = 0;
	for(var i = 0; i < data.length; i++)
	{
		if(String(data[i].date) == next_date)
			current_sum += data[i].hours;
		else
		{
			if(current_sum != 0)
			{
				entries.push(current_sum);
				expected_list.push(expected);
				dates.push(next_date);
			}
			next_date = data[i].date;
			current_sum = data[i].hours;
		}
	}
	if(data.length > 0)
	{
		entries.push(current_sum);
		expected_list.push(expected);
		dates.push(next_date);
	}

	$('#expected_chart').highcharts({
		chart: {
			zoomType: 'xy'
		},
		title: {
			text: ''
		},
		xAxis: [{
			categories: dates,
			labels: {
				rotation: -45,
				align: 'right'
			}
		}],
		yAxis: [{
			title: {
				text: 'Hours'
			}
		}],
		plotOptions: {
			series: {
				marker: {
					enabled: false
				}
			}
		},
		series: [{
			name: 'Reported Hours',
			color: '#76addb',
			type: 'column',
			data: entries
		}, {
			name: 'Expected Hours',
			color: '#ce0000',
			type: 'spline',
			data: expected_list
		}]
	});
}

function GetDistro()
{
	$.ajax({
		url: "../get_distribution",
		data: {start_date: today.getFullYear() + '-' + (today.getMonth()+1) + '-01', end_date: today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate()},
		dataType: 'json',
		success: function(data){
			SetupChart(data, "Your time so far this month:");
		},
		error: function(){
			alert("Failed to get time distribution!");
		}
	});	
}

var PROJECT_ENTRIES;
var TOTAL_HOURS = 0;

function SetupChart(data, title)
{
	var total = data.total;
	var entries = data.entries;
	PROJECT_ENTRIES = entries;
	TOTAL_HOURS = total;

	var data_list = new Array();

	for(var i = 0; i < entries.length; i++)
	{
		var entry = new Array(entries[i].name, ((entries[i].hours / total) * 100), entries[i].hours);
		data_list.push(entry);
	}

	var main_chart = new Highcharts.Chart({
		chart: {
                        renderTo: 'chart',
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false,
                        backgroundColor: 'rgba(255, 255, 255, 0.0)'
                },
                title: {
                        text: ''
                },
                tooltip: {
                        formatter: function(){
                                for(var i = 0; i < data_list.length; i++)
                                {
                                        if(data_list[i][0] == this.point.name)
                                                return '<b>'+this.point.name + '</b>: '+parseFloat(Math.round(data_list[i][1] * 100)/100).toFixed(1) + '%<br>'+data_list[i][2] + ' hours';
                                }
                                return this.point.name + ': ' + this.point.percentage + '%';
                        }
                },
                plotOptions:{
                        pie: {
                                allowPointSelect: true,
                                cursor: 'pointer',
                                dataLabels: {
                                        enabled: true,
                                        color: '#000000',
                                        connectorColor: '#000000',
                                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                                }
                        }
                },
                series: [{
                        type: 'pie',
                        name: 'Time Distribution',
                        data: data_list
                }],

	});
}

