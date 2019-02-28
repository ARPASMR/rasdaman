<%@page import="org.rasdaman.SecoreFilter"%>
<%@page import="org.rasdaman.secore.ConfigManager"%>
<!--
/*
 * This file is part of rasdaman community.
 *
 * Rasdaman community is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Rasdaman community is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU  General Public License for more details.
 *
 * You should have received a copy of the GNU  General Public License
 * along with rasdaman community.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright 2003 - 2014 Peter Baumann / rasdaman GmbH.
 *
 * For more information please see <http://www.rasdaman.org>
 * or contact Peter Baumann via <baumann@rasdaman.com>.
-->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></meta>

    <!-- Bootstrap Core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <style>
        .panel-heading a:after {
            font-family: 'Glyphicons Halflings';
            content: "\e114";
            float: right;
            color: grey;
        }
        
        .panel-heading a.collapsed:after {
            content: "\e080";
        }
        
        .center-block {
            width: 500px;
            padding: 10px;
        }
    </style>

    <title>Rasdaman.org - SECORE administration pages login</title>
    <link rel="shortcut icon" type="image/png" href="http://rasdaman.org/chrome/site/favicon.ico" />

    <script>
        function isEmpty(str) {
            return (!str || 0 === str.length);
        }

        // Check username and password is not empty
        function checkIsEmpty() {
            var username = document.getElementById("<%= SecoreFilter.USERNAME %>");
            var passWord = document.getElementById("passWord");

            var valid = false;

            if (isEmpty(username.value)) {
                alert("Username is not empty.");
            } else if (isEmpty(passWord.value)) {
                alert("Password is not empty.");
            } else {
                valid = true;
            }
            return valid;
        }
    </script>

</head>

<body>

    <div class="container" style="margin-top:10%;">

        <div class="center-block">

            <div class="panel panel-default" id="panel1">
                <div class="panel-heading">
                    <h4 class="panel-title">
                            <a data-toggle="collapse" data-target="#collapseOne" >
                                Login to SECORE administration interface
                            </a>
                        </h4>

                </div>
                <div id="collapseOne" class="panel-collapse collapse in">
                    <h5 style="text-align:center;color:red;">
                            <%
                            Object isSuccess = request.getAttribute(SecoreFilter.CLIENT_SUCCESS_ATTRIBUTE);                            
                            if (isSuccess != null && isSuccess.toString().equals("false")) {
                                out.print("Login unsuccessful (Username or Password is not valid)");
                            }
                            %>
                        </h5>
                    <div class="panel-body" style="margin-left:140px;">

                        <form method="post" action="<%= request.getAttribute(SecoreFilter.CLIENT_REQUEST_URI_ATTRIBUTE) %>">
                            <p>
                                <input type="text" id="<%= SecoreFilter.USERNAME %>" name="<%= SecoreFilter.USERNAME %>" value="" placeholder="Username">
                            </p>
                            <p>
                                <input type="<%= SecoreFilter.PASSWORD %>" id="<%= SecoreFilter.PASSWORD %>" name="<%= SecoreFilter.PASSWORD %>" value="" placeholder="Password">
                            </p>
                            <p class="submit" style="margin-top:10px;">
                                <input type="submit" name="login" value="Login" onclick="return checkIsEmpty();">
                            </p>
                        </form>
                    </div>
                </div>

            </div>
</body>

</html>