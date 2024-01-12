function send_form(endpoint, method)
{
    // Setting up the form
    const form = document.createElement('form');
    form.method = method;
    form.action = endpoint;
    // Getting the value in the writer
    var git_url = document.getElementById('git-url').value;
    if (git_url)
    {
        // Creating hidden field
        const hidden_field_url = document.createElement('input');
        hidden_field_url.type = 'hidden';
        hidden_field_url.name = 'git_url';
        hidden_field_url.value = git_url
        // Appending to the form
        form.appendChild(hidden_field_url);
    }
    else
    {
        document.getElementById("git-form").classList.add("was-validated");
        return;
    }
    // Appending the form to the body
    document.body.appendChild(form);
    // Submitting
    form.submit();
}

function explore()
{
    send_form("/", 'GET');
}

function bug_report()
{
    alert("Thanks for the report")
    send_form("/report.php", 'POST');
}

document.getElementById("explore-button").addEventListener("click", explore);
document.getElementById("bug-report-button").addEventListener("click", bug_report);