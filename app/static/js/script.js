var bodyClass = document.body.className;

// function to toggle between light and dark mode
function applyTheme(theme) {
    document.body.classList.remove("theme-auto", "theme-light", "theme-dark", "theme-undefined");
    document.body.classList.add(`theme-${theme}`);
    var bodyClass = document.body.className;
    document.documentElement.setAttribute("theme", `theme-${theme}`);
    
    // Create a new XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // Define the request method, URL, and set it to be asynchronous
    xhr.open("POST", "/endpoint", true);

    // Set the request header if needed (e.g., if sending data as JSON)
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // Define a callback function to handle the response from the server
    xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
        console.log("Server response:", xhr.responseText);
        } else {
        console.error("Error: " + xhr.status);
        }
    }
    };
    // Prepare the data to be sent (in this case, as a JSON string)
    var data = JSON.stringify({ bodyClass: bodyClass });

    // Send the request with the data
    xhr.send(data);
}

console.log(document.body.className)

document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme") || "auto";

    applyTheme(savedTheme);

    for (const optionElement of document.querySelectorAll("#selTheme option")) {
    optionElement.selected = savedTheme === optionElement.value;
    }

    document.querySelector("#selTheme").addEventListener("change", function () {
    localStorage.setItem("theme", this.value);
    applyTheme(this.value);
    });
});

const daysTag = document.querySelector(".days"),
currentDate = document.querySelector(".current-date"),
prevNextIcon = document.querySelectorAll(".icons span");

// getting new date, current year and month
let date = new Date(),
currYear = date.getFullYear(),
currMonth = date.getMonth();

// storing full name of all months in array
const months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];


const renderCalendar = () => {
    let firstDayofMonth = new Date(currYear, currMonth, 1).getDay(), // getting first day of month
    lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(), // getting last date of month
    lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(), // getting last day of month
    lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate(); // getting last date of previous month
    let liTag = "";

    for (let i = firstDayofMonth; i > 0; i--) { // creating li of previous month last days
        liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
    }

 // function to get event colour to display in calendar
function getEventColour(day, events) {
    const event = events.find(event => {
        const eventDate = new Date(event.date);
        const eventDay = eventDate.getDate();
        const eventMonth = eventDate.getMonth();
        const eventYear = eventDate.getFullYear();
        return eventDay === day && eventMonth === currMonth && eventYear === currYear;
        
    });
    return event ? event.colour : "";
    }


function loadEvents() {
    for (let i = 1; i <= lastDateofMonth; i++) { // creating li of all days of current month
        // adding active class to li if the current day, month, and year matched
       let isToday = i === date.getDate() && currMonth === new Date().getMonth() && currYear === new Date().getFullYear() ? "active" : "";
       let hasEvent = false;
       let currDateYear = new Date(currYear, currMonth, i).getFullYear();
       let currDateMonth = new Date(currYear, currMonth, i).getMonth() + 1;
       let currDateDay = new Date(currYear, currMonth, i).getDate();
       // need month and day to be in format 0x e.g. 09 not 9
       if (currDateMonth < 10 && currDateDay < 10) {
        var formattedDate = `${currDateYear}-0${currDateMonth}-0${currDateDay}`
       }
       else if (currDateMonth < 10) {
        var formattedDate = `${currDateYear}-0${currDateMonth}-${currDateDay}`
       }
       else if (currDateDay < 10) {
        var formattedDate = `${currDateYear}-${currDateMonth}-0${currDateDay}`
       }
       else {
        var formattedDate = `${currDateYear}-${currDateMonth}-${currDateDay}`
       }
        events.forEach(event => {
            const eventDate = new Date(event.date);
            const eventDay = eventDate.getDate();
            const eventMonth = eventDate.getMonth();
            const eventYear = eventDate.getFullYear();
    
            if (eventDay === i && eventMonth === currMonth && eventYear === currYear) {
                hasEvent = true;
            }
         });
 
         if (hasEvent == true) {
             colour = getEventColour(i, events)
             liTag += `<li style = "color: ${getEventColour(i, events)}" class="${"eventDay"}${isToday}${hasEvent ? " event" : ""}">\n${`<a href = "/calendar/${formattedDate}"> ${i} </a>`}</li>`;
             var styleElem = document.head.appendChild(document.createElement("style"));
             styleElem.innerHTML = ".days li.eventDay::before {border-style: solid; border-color: ${colour}};}";
         }
         else {
             liTag += `<li class="${isToday}${hasEvent ? " event" : ""}">\n${`<a href = "/calendar/${formattedDate}"> ${i} </a>`}</li>`;
         } 
        
   }

   for (let i = lastDayofMonth; i < 6; i++) { // creating li of next month first days
    liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`
    }

    currentDate.innerText = `${months[currMonth]} ${currYear}`; // passing current mon and yr as currentDate text
    daysTag.innerHTML = liTag;
}

    let events = [];

    async function fetchData() {
        try {
            const response = await fetch('/data.json');
            const data = await response.json();
            events = data;
        } catch (error) {
            console.log(error);
        }
    }

    fetchData().then(() => {
        // Access the modified value of 'events' here
        // TODO: Load calendar here...
        console.log(events)
        loadEvents();
    });
    
}
renderCalendar();

prevNextIcon.forEach(icon => { // getting prev and next icons
    icon.addEventListener("click", () => { // adding click event on both icons
        // if clicked icon is previous icon then decrement current month by 1 else increment it by 1
        currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;

        if(currMonth < 0 || currMonth > 11) { // if current month is less than 0 or greater than 11
            // creating a new date of current year & month and pass it as date value
            date = new Date(currYear, currMonth, new Date().getDate());
            currYear = date.getFullYear(); // updating current year with new date year
            currMonth = date.getMonth(); // updating current month with new date month
        } else {
            date = new Date(); // pass the current date as date value
        }
        renderCalendar(); // calling renderCalendar function
    });
});

function openForm() {
  document.getElementById("myForm").style.display = "block";
}

// If I have time: close other forms when one is opened
function openEditForm(eventID) {
    var formID = "myEditForm" + eventID;
    document.getElementById(formID).style.display = "block";
  }

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

function closeEditForm(eventID) {
    var formID = "myEditForm" + eventID;
    document.getElementById(formID).style.display = "none";
  }

function openTaskEditForm(taskID) {
    var formID = "myEditForm" + taskID;
    document.getElementById(formID).style.display = "block";
}

function closeTaskEditForm(taskID) {
    var formID = "myEditForm" + taskID;
    document.getElementById(formID).style.display = "none";
}

// Progress bar

// Get the number of circles (tasks) and the number of tasks completed
const progress = document.getElementById("progress");
const circles = document.querySelectorAll(".circle");

// Update the progress bar
const update = () => {
    const actives = document.querySelectorAll(".active");
    progress.style.width = ((actives.length - 1) / (circles.length - 1)) * 100 + "%";
}

update();


