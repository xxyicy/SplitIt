/** namespace. */
var rh = rh || {};
rh.splitit = rh.splitit || {};

rh.splitit.sharedInit = function() {
	// Dialog Polyfill for browsers that don't support the dialog tag.
	var dialogs = document.querySelectorAll('dialog');
	for (var i = 0; i < dialogs.length; i++) {
		// Using an old school style for loop since this for compatibility.
		var dialog = dialogs[i];
		if (!dialog.showModal) {
			dialogPolyfill.registerDialog(dialog);
		}
	}

	$(".close-parent-dialog").click(function() {
		var dialogEl = $(this).closest("dialog").get(0);
		dialogEl.close();
	});
};

rh.splitit.profilePageInit = function() {
	$("#edit-btn").click(function() {
		$(".info-div").removeClass("hidden");
		$(".info-label").addClass("hidden");
		$("#cancel-btn").removeClass("hidden");
		$("#save-btn").removeClass("hidden");
		$("#edit-btn").addClass("hidden");
	})

	$('#cancel-btn').click(function() {
		$(".info-div").addClass("hidden");
		$(".info-label").removeClass("hidden");
		$("#cancel-btn").addClass("hidden");
		$("#save-btn").addClass("hidden");
		$("#edit-btn").removeClass("hidden");
	})

	$("#save-btn").click(function() {
		$(".info-div").addClass("hidden");
		$(".info-label").removeClass("hidden");
		$("#cancel-btn").addClass("hidden");
		$("#save-btn").addClass("hidden");
		$("#edit-btn").removeClass("hidden");
	})
}

rh.splitit.groupsPageInit = function() {
	// Insert Group - Create
	$("#add-group-btn").click(function() {
		document.querySelector('#add-group-dialog').showModal();
	});

	// Attach an event listener to the modal
	$('#add-group-dialog').on('shown.bs.modal', function() {
		$("input[name='name']").focus();
	});


	// Insert Group - Edit
	$(".group-card").click(function() {
		var groupKey = $(this).find(".entity-key").html();
		window.location.replace("/events?group_key=" + groupKey);
	});
};

rh.splitit.groupPageInit = function() {
	  // Edit list name
	  $("#edit-group-info-btn").click(function() {
	    document.querySelector('#edit-group-info-dialog').showModal();
	  });
	  // Close the list rename modal and update the page title.
	  $("#done-editing-group-info").click(function() {
	    var name = $("input[name=groupName]").val();
	    var description = $("input[name=groupDescription").val();
	    $("#group-name").text(name);
	    $("#group-description").text(description);
	    $("input[name=group_name]").val(name);
	    $("input[name=group_description").val(description);
	  });
	  
	  // Related to Deleting a List
	  $("#delete-group-btn").click(function() {
	    document.querySelector("#delete-group-dialog").showModal();
	  });
	  
	  $("#back-group-btn").click(function() {
		  var groupKey = $("input[name=group_entity_key]").val();
		  window.location.replace("/events?group_key=" + groupKey);
	  })
	  
	$(".concise-friend-card").click(function() {
		var finished = $("input[name=group_finished]").val();
		var entityKey = $(this).find(".entity-key").html();
		if (finished){
			var groupKey = $("input[name=group_entity_key]").val();
			console.log(groupKey)
			window.location.replace("/group/user_expense?user_key="+entityKey+"&group_key="+groupKey)
		}else if ($("input[name=user_key]").val() === $("input[name=group_parent_key]").val()){
			$elem = $(this);
			var isInListBeforeClick = $elem.parents(".friends-in-group").length > 0;
			var hasMovedClass = $elem.hasClass("moved-contact");
			groupKeysToAddString = $("input[name=group_keys_to_add]").val();
			groupKeysToRemoveString = $("input[name=group_keys_to_remove]").val();
	
			$elem.detach();
			if (isInListBeforeClick && hasMovedClass) {
				$elem.appendTo(".friends-not-in-group > .mdl-grid").removeClass("moved-contact");
				groupKeysToAddString = rh.splitit.toggleStringInList(groupKeysToAddString,entityKey);
			} else if (isInListBeforeClick && !hasMovedClass) {
				$elem.appendTo(".friends-not-in-group > .mdl-grid").addClass("moved-contact");
				groupKeysToRemoveString = rh.splitit.toggleStringInList(groupKeysToRemoveString,entityKey);
			} else if (!isInListBeforeClick && hasMovedClass) {
				$elem.appendTo(".friends-in-group > .mdl-grid").removeClass("moved-contact");
				groupKeysToRemoveString = rh.splitit.toggleStringInList(groupKeysToRemoveString,entityKey);
			} else if (!isInListBeforeClick && !hasMovedClass) {
				$elem.appendTo(".friends-in-group > .mdl-grid").addClass("moved-contact");
				groupKeysToAddString = rh.splitit.toggleStringInList(groupKeysToAddString,entityKey);
			}
			$("input[name=group_keys_to_add]").val(groupKeysToAddString);
			$("input[name=group_keys_to_remove]").val(groupKeysToRemoveString);
		}else {
			console.log($("input[name=user_key]").val())
			console.log($("input[name=group_parent_key]").val())
		}
	});
}

rh.splitit.eventsPageInit = function() {
	// Insert Event - Create
	$("#add-event-btn").click(function() {
		document.querySelector('#add-event-dialog').showModal();
	});

	// Attach an event listener to the modal
	$('#add-event-dialog').on('shown.bs.modal', function() {
		$("input[name='name']").focus();
	});
	
	$('#edit-group-btn').click(function() {
		var groupKey = $("input[name=group_entity_key]").val();
		window.location.replace("/group?group_key=" + groupKey);
	})

	// Insert Event - Edit
	$(".event-card").click(function() {
		var eventKey = $(this).find(".entity-key").html();
		var groupKey = $("input[name=group_entity_key]").val();
		
		window.location.replace("/event?event_key=" + eventKey +"&group_key="+groupKey);
	});
	
	$(".event-edit-btn").click(function() {
		var eventKey = $(".event-card").find(".entity-key").html();
		var groupKey = $("input[name=group_entity_key]").val();
		
		window.location.replace("/event?event_key=" + eventKey +"&group_key="+groupKey);
	});
	
	$(".go-back-to-events-btn").click(function(){
		var groupKey = $("input[name='group_key']").val();
		
		window.location.replace("/events?group_key=" + groupKey);
	})
	
	$("#finish-group-btn").click(function(){
		var groupKey = $("input[name='group_entity_key']").val();
		console.log(groupKey)
		window.location.replace("/finish-group?group_key="+groupKey)
	})
	
};

rh.splitit.eventPageInit = function() {
	// Edit list name
	  $("#edit-event-info-btn").click(function() {
	    document.querySelector('#edit-event-info-dialog').showModal();
	  });
	  // Close the list rename modal and update the page title.
	  $("#done-editing-event-info").click(function() {
	    var name = $("input[name=eventName]").val();
	    var description = $("input[name=eventDescription").val();
	    var cost = $("input[name=eventTotalCost").val();
	    $("#event-name").text(name);
	    $("#event-description").text(description);
	    $("#event-totalCost").text(cost);
	    $("input[name=event_name]").val(name);
	    $("input[name=event_description").val(description);
	    $("input[name=event_totalCost").val(cost);
	  });
	  
	  // Related to Deleting a List
	  $("#delete-event-btn").click(function() {
	    document.querySelector("#delete-event-dialog").showModal();
	  });
	  
	  $("#back-event-btn").click(function() {
		  var groupKey = $("input[name=event_entity_key]").val();
		  window.location.replace("/events?group_key=" + groupKey);
	  })
	  
	
	$(".concise-friend-card").click(function() {
		if ($("input[name=user_key]").val() === $("input[name=event_parent_key]").val()){
			$elem = $(this);
			var isInListBeforeClick = $elem.parents(".friends-in-event").length > 0;
			var hasMovedClass = $elem.hasClass("moved-contact");
			var entityKey = $(this).find(".entity-key").html();
			eventKeysToAddString = $("input[name=event_keys_to_add]").val();
			eventKeysToRemoveString = $("input[name=event_keys_to_remove]").val();
	
			$elem.detach();
			var userInfo = {
					key: $elem.find(".entity-key").html(),
					nickname: $elem.find(".contact-nickname").html(),
					phoneNumber: $elem.find(".friend-phonenumber").html(),
					email: $elem.find(".friend-email").html()
				};
			if (isInListBeforeClick && hasMovedClass) {
				$elem.appendTo(".friends-not-in-event > .mdl-grid").removeClass("moved-contact");
				eventKeysToAddString = rh.splitit.toggleStringInList(eventKeysToAddString,entityKey);
				$('#tr'+userInfo.key).addClass("hide");
			} else if (isInListBeforeClick && !hasMovedClass) {
				$elem.appendTo(".friends-not-in-event > .mdl-grid").addClass("moved-contact");
				eventKeysToRemoveString = rh.splitit.toggleStringInList(eventKeysToRemoveString,entityKey);
				$('#tr'+userInfo.key).addClass("hide");
			} else if (!isInListBeforeClick && hasMovedClass) {
				$elem.appendTo(".friends-in-event > .mdl-grid").removeClass("moved-contact");
				eventKeysToRemoveString = rh.splitit.toggleStringInList(eventKeysToRemoveString,entityKey);
				$('#tr'+userInfo.key).removeClass("hide");
			} else if (!isInListBeforeClick && !hasMovedClass) {
				$elem.appendTo(".friends-in-event > .mdl-grid").addClass("moved-contact");
				eventKeysToAddString = rh.splitit.toggleStringInList(eventKeysToAddString,entityKey);
				$('#tr'+userInfo.key).removeClass("hide");
			}
			$("input[name=event_keys_to_add]").val(eventKeysToAddString);
			$("input[name=event_keys_to_remove]").val(eventKeysToRemoveString);
			
		}else {
			console.log($("input[name=user_key]").val())
			console.log($("input[name=event_parent_key]").val())
		}
	});
	  
	  $("#split-event-btn").click(function(){
		  var totalCost = parseFloat($("#event-totalCost").text())
		  var elements = $("tr[class$='exp-tr']");
		  elements.each(function() {
			  var text = $(this).find("#cost").html();
			  var cost = parseFloat(text);
			  if (!cost && cost!= 0) {
				  alert("Please enter correct number!");
				  return;
			  }
			  totalCost-=cost;
		  });
		  var elements2 = $("tr[class$='exp-tr is-selected'] ");
		  elements2.each(function() {
			  $(this).find("#cost").html(totalCost/elements2.length);
		  });
		  
	  })
	  
	  $("#clear-expenses-btn").click(function(){
		  var elements = $("tr");
		  elements.each(function() {
			  $(this).find("#cost").html("0.0");
		  });
	  })
	  
	  
	  $("#save-event-btn").click(function(){
		  var event_name = $('input[name="event_name"').val();
		  var event_description = $('input[name="event_description"]').val();
		  var event_totalCost = $('input[name="event_totalCost"]').val();
		  var urlsafe_entity_key = $('input[name="event_entity_key"]').val();
		  var urlsafe_event_keys_to_add = $('input[name="event_keys_to_add"]').val();
		  var urlsafe_event_keys_to_remove = $('input[name="event_keys_to_remove"]').val();
		  
		  var eventCost = parseFloat($("#event-totalCost").text());
		  var totalCost = eventCost;
		  var expenses = [];
		  var elements = $("tr[class$='exp-tr']");
		  elements.each(function() {
			  var text = $(this).find("#cost").html();
			  var cost = parseFloat(text);
			  if (!cost && cost!= 0) {
				  alert("Please enter correct number on expenses table!");
				  return;
			  }
			  var expense_key = $(this).find("#cost").attr("class");
			  var elemID = $(this).attr("id")
			  var person_key = elemID.substring(2, elemID.length);
			  var expense = {
					expense_key: expense_key,
					person_key: person_key,
					cost: cost
			  		}
			  expenses.push(expense);
			  totalCost-=cost;
		  });
		  var elements2 = $("tr[class$='exp-tr is-selected']");
		  elements2.each(function() {
			  var text = $(this).find("#cost").html();
			  var cost = parseFloat(text);
			  if (!cost && cost!= 0) {
				  alert("Please enter correct number expenses table!");
				  return;
			  }
			  var expense_key = $(this).find("#cost").attr("class");
			  var elemID = $(this).attr("id")
			  var person_key = elemID.substring(2, elemID.length);
			  var expense = {
					expense_key: expense_key,
					person_key: person_key,
					cost: cost  
			  		}
			  expenses.push(expense);
			  totalCost-=cost;
		  });
		  
		  console.log(totalCost);
		  if (totalCost < -0.00001 || totalCost > 0.00001){
			  alert("Expenses are not equal to total cost!");
			  return;
		  }
		  
		  var data = {
				event_name: event_name,
				event_description: event_description,
				event_totalCost: event_totalCost,
				event_entity_key: urlsafe_entity_key,
				event_keys_to_add: urlsafe_event_keys_to_add,
				event_keys_to_remove: urlsafe_event_keys_to_remove,
				expenses: JSON.stringify(expenses)
		  }
		  console.log(data);
		  $.ajax({
              url: "/update-event",
              type: 'POST',
              data: data,
              dataType: 'JSON',
              success: function (data) {
            	  if (!data){
            		  return
            	  }
            	  console.log(data);
                  window.location.reload();
              },
              error: function (request, status, error) {
                  console.log(error);
              }
          });
		  
	  })

}

/* Helper methods */
rh.splitit.toggleStringInList = function(stringList, stringToToggle) {
  if (stringList.indexOf(stringToToggle) > -1) {
    // Present. Remove it.
    var res = stringList.replace(stringToToggle, "");
    res = res.replace(",,", ",");
    var trim = res.replace(/(^,)|(,$)/g, ""); // from
    // http://stackoverflow.com/questions/661305/how-can-i-trim-the-leading-and-trailing-comma-in-javascript
    return trim;
  } else {
    // Not present. Add it.
    if (stringList.length > 0) {
      return stringList + "," + stringToToggle;
    } else {
      return stringToToggle;
    }
  }
};

/* Main */
$(document).ready(function() {
	rh.splitit.sharedInit();
	rh.splitit.profilePageInit();
	rh.splitit.groupsPageInit();
	rh.splitit.groupPageInit();
	rh.splitit.eventsPageInit();
	rh.splitit.eventPageInit();
});