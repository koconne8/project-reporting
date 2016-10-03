// localStorage name used to keep track of which projects are selected
var LOCAL_STORAGE_KEY_NAME = 'redmineReport';


// Main function that is called once the page is loaded.
// This function selects the previous month for the user automatically.
// It also sets an "onchange" event for each checkbox - this is used to keep track, using local storage, the selected items.
function init()
{
	//------------- Setting up Previous Month ------------------//
	var now = new Date();
	prev_month = now.getMonth() - 1;
	var year_offset = 0;
	if(prev_month < 0)
	{
		prev_month = 11;
		year_offset = 1;
	}
	prev_year = now.getFullYear() - year_offset;

	// offset the month (since the Date object says January = 0 and December = 11)
	prev_month = prev_month + 1;

	// now select last month from the drop-down list
	$('#month').val(prev_month);

	// and now select the year (if previous year, it'll update for that too)
	$('#year').val(prev_year);


	//-------------- Setup Onchange Events for Checkboxes ------------------//
	// check to see if our local storage has a "redmineReport" element, and if not, create one.
	if(localStorage[LOCAL_STORAGE_KEY_NAME]  == undefined)
	{
		var no_projects_selected = new Array();
		localStorage[LOCAL_STORAGE_KEY_NAME] = JSON.stringify(no_projects_selected);
	}



	// for each project's checkbox... 
	$('[name="project_choice"]').each(function(){
		// add a new function for the change event
		$(this).change(function(){
			//console.log("state changed: " + $(this).attr('id'));
			// get the current list of objects
			var selected_projects = JSON.parse(localStorage[LOCAL_STORAGE_KEY_NAME]);
	
			// if we just checked this object, we add it
			if($(this).attr('checked') == 'checked')
				selected_projects.push($(this).attr('id'));
			else
			{
				// find where our id is and remove it
				for(var i = 0; i < selected_projects.length; i++)
				{
					if(selected_projects[i] == $(this).attr('id'))
					{
						selected_projects.splice(i, 1);
						break;
					}
				}
				// also, make sure the "All Projects" checkbox is unchecked!
				$('#check_all_box').removeAttr('checked');
			}
			localStorage[LOCAL_STORAGE_KEY_NAME] = JSON.stringify(selected_projects);

			// now do all of our children!
			CheckChildren(this.id, $(this).attr('checked'));
		});
	});

	//--------------- Setup Onchange Events for Month/Year Selections ----------------------------------//
	$('#month').change(function(){
		// grab an updated missing hour count
		$.ajax({
			url: '../missing_hours',
			data: {month: $('#month').val(), year: $('#year').val()},
			dataType: "text",
			success: function(missing_hours){
				$('#missing_hour_count').html(missing_hours);
			},
			error: function(){
				alert("Could not retrieve unassigned hours.");
			}
		});
	});

	$('#year').change(function(){
		// grab an updated missing hour count
		$.ajax({
			url: '../missing_hours',
			data: {month: $('#month').val(), year: $('#year').val()},
			dataType: "text",
			success: function(missing_hours){
				$("#missing_hour_count").html(missing_hours);
			},
			error: function(){
				alert("Could not retrieve unassigned hours.");
			}
		});
	});
	
	//--------------------- Auto-select projects we've selected before ---------------------------------//
	// get the list of selected projects
	var selected_projects = JSON.parse(localStorage[LOCAL_STORAGE_KEY_NAME]);
	
	// for each one, check that checkbox!
	for(var i = 0; i < selected_projects.length; i++)
		$('#'+selected_projects[i]).attr('checked', 'checked');


	//------------------- Add POST Submission to Generate Button ---------------------------------------//
	$('#internal_button').click(function(){
		// submit to have our stuff generated!
		var list = [];
		$('[name="project_choice"]').each(function(){
			if($(this).is(':checked')){
				list.push($(this).attr('id'));
			}
		});
		window.location.href = '../generate_internal_report?ProjectList='+list+'&month='+$('#month').val()+'&year='+$('#year').val()+'&all_projects='+$('#check_all_box').attr('checked');
	});

	$('#external_button').click(function(){
		// submit to gather all external-only information
		$('[name="project_choice"]').each(function(){
			if($(this).is(':checked')){
				list.push($(this).attr('id'));
			}
		});
		window.location.href = '../generate_external_report?ProjectList='+list+'&month='+$('#month').val()+'&year='+$('#year').val()+'&all_projects='+$('#check_all_box').attr('checked');
	});

	$('#csr_button').click(function(){
		// submit to gather all external-only information
		$('[name="project_choice"]').each(function(){
			if($(this).is(':checked')){
				list.push($(this).attr('id'));
			}
		});
		window.location.href = '../generate_csr_report?ProjectList='+list+'&month='+$('#month').val()+'&year='+$('#year').val()+'&all_projects='+$('#check_all_box').attr('checked');
	});

	$('#check_all_box').change(function(){
		// reset the local storage
		selected_projects = new Array();

		var state = this.checked;

		// run through all checkboxes and make them match our state
		$('[name="project_choice"]').each(function(){
			this.checked = state;
			if(state){
				selected_projects.push(this.id);
			}
		});

		// for(var i = 0; i < document.getElementsByName('project_choice').length; i++)
		// {
		// 	$('#'+document.getElementsByName('project_choice')[i].id).attr('checked', this.checked);
		// 	// if checked, add it
		// 	if(this.checked == true)
		// 		selected_projects.push(document.getElementsByName('project_choice')[i].id);
		// }
	
		localStorage[LOCAL_STORAGE_KEY_NAME] = JSON.stringify(selected_projects);
	});

	// once all of this is setup, make sure our children are kept in line!
	//FamilyReunion();
}

// This function finds the children of any given project and pushes them to the left (CSS) of their parent
function FamilyReunion()
{
	// Run through all inputs, looking for parent ids that are NOT '-1'
	for(var i = 0; i < document.getElementsByName('project_choice').length; i++)
	{
		// check if they have a parent
		if($('#'+document.getElementsByName('project_choice')[i].id).attr('parent_id') != '-1')
		{
			// push it 10 pixels to the left of its parent
			
			// get parent id
			var parent_id = $('#'+document.getElementsByName('project_choice')[i].id).attr('parent_id');
		
			// calculate 20 pixels left (and prepare for CSS syntax)
			var left = String(parseInt($('#'+parent_id).css('margin-left').slice(0, -2))+20)+'px';
	
			// move our child over to the left 10 pixels
			$('#'+document.getElementsByName('project_choice')[i].id).css('margin-left', left);

			// because this is a child, shrink the font a tad...
			$('#label_'+document.getElementsByName('project_choice')[i].id).css('font-size', 'small');
			$('#label_'+document.getElementsByName('project_choice')[i].id).css('text-transform', 'uppercase');
		}
		else
		{
			// otherwise, make it BOLD
			$('#label_'+document.getElementsByName('project_choice')[i].id).css('font-weight', 'bold');
		}
	}
}

// Recursive function that checks all children whose parent_id matches the one passed in,
// then for each child, calls the same function passing in this child's ID (so all grand-children, etc get checked)
function CheckChildren(parent_id, state)
{
	// Run through all inputs, looking for parent ids that are NOT '-1'
	for(var i = 0; i < document.getElementsByName('project_choice').length; i++)
	{
		// check if they have a parent
		if($('#'+document.getElementsByName('project_choice')[i].id).attr('parent_id') == parent_id)
		{
			// check this child if state is defined
			if(state != undefined)
				$('#'+document.getElementsByName('project_choice')[i].id).attr('checked', state);
			else
				$('#'+document.getElementsByName('project_choice')[i].id).removeAttr('checked');

			// get the current list of objects
			var selected_projects = JSON.parse(localStorage[LOCAL_STORAGE_KEY_NAME]);
	
			// if we just checked this object, we add it
			if(state == 'checked')
				selected_projects.push($('#'+document.getElementsByName('project_choice')[i].id).attr('id'));
			else
			{
				// find where our id is and remove it
				for(var j = 0; j < selected_projects.length; j++)
				{
					if(selected_projects[j] == $('#'+document.getElementsByName('project_choice')[i].id).attr('id'))
					{
						selected_projects.splice(j, 1);
						break;
					}
				}
			}
			localStorage[LOCAL_STORAGE_KEY_NAME] = JSON.stringify(selected_projects);

			// make sure all of this child's children (grand-children) are checked
			CheckChildren($('#'+document.getElementsByName('project_choice')[i].id).attr('id'), state);
		}
	}
}
