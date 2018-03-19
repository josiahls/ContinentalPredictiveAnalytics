<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    
</head>
<body>
<h1>Continental HR Predictive Analytics

<h1>Dev Setup</h1>
<h3>Coding Conventions</h3>
<ul>
    <h4>Python ref <a>https://github.com/pandas-dev/pandas</a></h4>
    <ul>
        <li>Methods: named_like_this <b><i>note they might have __name__ for built in util methods</i></b>
        <li>variables: named_like_this
        <li>constants: NAMED_LIKE_THIS
        <li>file (and directory) names: named_like_this
        <li>class names: ObjectIsThis</li>
        <li>unit test class names: test_ObjectBeingTested
        <li>unit tests (test methods): test_method_test_name <b>note these must have <i>test_</i> at the start of their name</b>
    </ul>
    <h4>MySQL (DB) <a>https://stackoverflow.com/questions/7899200/is-there-a-naming-convention-for-mysql</a></h4>
        <ul>
        <li>table names: named_like_this
        <li>columns: named_like_this_detail <b><i>note 'detail' might be _id, _fk, _pk ect..</i></b>
        <li>triggers: named_like_this_tg
    </ul>
</ul>
<h3>Tools</h3>
<ul>
    <li>Pycharm 2017.1.5</li>
    <li><b>If using windows os: </b> cmder</li>
    <li>Python 3.6 (Anaconda3)</li>
    <li>Travis-ci yml needs to be present</li>
</ul>

<h3>Installation</h3>
<ul>
    <li>
        If using windows, use cmder and nav to Anaconda3/Scripts/pip
        <a>https://plot.ly/dash/getting-started#installation</a>
        <ul>
        <li>
        pip install dash  # The core dash backend
        <li>
        pip install dash-renderer==0.9.0 # The dash front-end
        <li>
        pip install dash-html-components # HTML components
        <li>
        pip install dash-core-components==0.13.0-rc4  # Supercharged components
        <li>
        pip install plotly --upgrade  # Latest Plotly graphing library
    </li>
</ul>

</body>
</html>
