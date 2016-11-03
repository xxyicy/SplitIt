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
		if ($("input[name=user_key]").val() === $("input[name=group_parent_key]").val()){
			$elem = $(this);
			var isInListBeforeClick = $elem.parents(".friends-in-group").length > 0;
			var hasMovedClass = $elem.hasClass("moved-contact");
			var entityKey = $(this).find(".entity-key").html();
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
};

rh.splitit.eventPageInit = function() {
	
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