let dom = {
    wordInput : null,
    genericPOSInput : null,
    domainPOSInput : null,
    searchButton : null,
    clearButton : null,

    updateButton : null,
    makeGenericDBButton : null,
    makeDomainDBButton : null,

    dicInfoDetailsLeft : null,
    dicInfoDetailsRight : null,
    dicInfoDetails : null,

    loadingBox: null
};

/**
 * body onload = "init()"
 */
function init() {
    getDomReferences();
    registerListeners();
}

/**
 * dom 객체 레퍼런스를 가져온다.
 */
function getDomReferences() {
    dom.wordInput = document.getElementById("wordInput");
    dom.genericPOSInput = document.getElementById("genericPOSInput");
    dom.domainPOSInput = document.getElementById("domainPOSInput");
    dom.searchButton = document.getElementById("searchButton");
    dom.clearButton = document.getElementById("clearButton");

    dom.dicInfoDetails = document.getElementById("dicInfoDetails");
    dom.updateButton = document.getElementById("updateButton");
    dom.makeGenericDBButton = document.getElementById("MakeGenericButton");
    dom.makeDomainDBButton = document.getElementById("MakeDomainButton");

    dom.loadingBox = document.getElementById("loadingBox");
}

/**
 * 이벤트 리스너를 등록한다.
 */
function registerListeners() {
    dom.searchButton.addEventListener("click", onSearchButtonClick);
    dom.clearButton.addEventListener("click", onClearButtonClick);
    dom.updateButton.addEventListener("click", onUpdateButtonClick);
    dom.makeGenericDBButton.addEventListener("click", onMakeGenericDBButton);
    dom.makeDomainDBButton.addEventListener("click", onMakeDomainDBButton);
}
// input values initialize
function onClearButtonClick(){
    dom.wordInput.value = null;
    dom.genericPOSInput.value = null;
    dom.domainPOSInput.value = null;
    // dom.dicInfoDetailsLeft.value = null;
    // dom.dicInfoDetailsRight.value = null;
    dom.dicInfoDetails.value = null;
}

// loading box function
function showLoadingBox() {
    dom.loadingBox.style.display = "inline-block";
}

function hideLoadingBox() {
    dom.loadingBox.style.display = "none";
}


function onSearchButtonClick(){
    postSearch();
}


function onUpdateButtonClick(){
    postUpdate();
}


function onMakeGenericDBButton(){
    showLoadingBox();
    postMakeGenericDB();
}

function onMakeDomainDBButton(){
    showLoadingBox();
    postMakeDomainDB();
}

//Post function
//post - word, generic, domain
//response - dicInfoLeft, Right
function postSearch() {
    var data = {
        word : dom.wordInput.value,
        generics : dom.genericPOSInput.value,
        domains : dom.domainPOSInput.value
    };

    $.ajax({
        type: "POST",
        url: "/postSearch",
        data: JSON.stringify(data),
        dataType:'json' ,
        contentType: "application/json",
        success: function (response) {
            // if error has data => show error msg alert
            dom.dicInfoDetails.value = response.result;

            if (typeof(response.errors) != "undefined" && response.errors.length != 0 ) {
                alert((response.errors));
                dom.dicInfoDetails.value = response.errors;
            }
            // dom.dicInfoDetailsLeft.value = response.dicInfoLeft;
            //dom.dicInfoDetailsRight.value = response.dicInfoRight;
            // text.posTagged = response.result;
            // dom.dicInfoDetailsLeft.innerHTML = text.posTagged;

        }
    });
}

function postUpdate() {
    var data = {
        word : dom.wordInput.value,
        generics : dom.genericPOSInput.value,
        domains : dom.domainPOSInput.value,
        updateText : dom.dicInfoDetails.value
    };
    $.ajax({
        type: "POST",
        url: "/postUpdate",
        data: JSON.stringify(data),
        dataType:'json' ,
        contentType: "application/json",
        success: function (response) {
            // if error has data => show error msg alert
            alert(response.result)
            if (typeof(response.error) == 1) {
                alert((response.message));
                dom.dicInfoDetails.value = "";
            }
            // dom.dicInfoDetailsLeft.value = response.dicInfoLeft;
            //dom.dicInfoDetailsRight.value = response.dicInfoRight;
            // text.posTagged = response.result;
            // dom.dicInfoDetailsLeft.innerHTML = text.posTagged;

        }
    });
}


function postMakeGenericDB() {

    $.ajax({
        type: "POST",
        url: "/postMakeGenericDB",
        data: JSON.stringify({}),
        dataType:'json' ,
        contentType: "application/json",
        success: function (response) {
            // if error has data => show error msg alert
            dom.dicInfoDetails.value = response.result;
            hideLoadingBox();
/*
            if (typeof(response.errors) != "undefined" && response.errors.length != 0 ) {
                alert((response.errors));
                dom.dicInfoDetails.value = response.errors;
            }
            // dom.dicInfoDetailsLeft.value = response.dicInfoLeft;
            //dom.dicInfoDetailsRight.value = response.dicInfoRight;
            // text.posTagged = response.result;
            // dom.dicInfoDetailsLeft.innerHTML = text.posTagged;
*/
        }
    });
}

function postMakeDomainDB() {
    var data = {
        word : dom.wordInput.value,
        generics : dom.genericPOSInput.value,
        domains : dom.domainPOSInput.value
    };
    $.ajax({
        type: "POST",
        url: "/postMakeDomainDB",
        data: JSON.stringify(data),
        dataType:'json' ,
        contentType: "application/json",
        success: function (response) {
            // if error has data => show error msg alert
            hideLoadingBox();
            alert(response.result);
/*
            if (typeof(response.errors) != "undefined" && response.errors.length != 0 ) {
                alert((response.errors));
                dom.dicInfoDetails.value = response.errors;
            }
            // dom.dicInfoDetailsLeft.value = response.dicInfoLeft;
            //dom.dicInfoDetailsRight.value = response.dicInfoRight;
            // text.posTagged = response.result;
            // dom.dicInfoDetailsLeft.innerHTML = text.posTagged;
*/
        }
    });
}


