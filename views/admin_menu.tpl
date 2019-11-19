<html>
<head>
<script>
function showControls() {
    cmd = document.getElementById("command_list").value;
    if ((cmd != "put_pkeys") && (cmd != "put_ckeys"))
        document.getElementById("upload_keys").style.display = "none";
    else
        document.getElementById("upload_keys").style.display = "block";

    if ((cmd == "get_keys") || (cmd == "get_pkeys") || (cmd == "get_ckeys"))
        document.getElementById("last_updated_ts").style.display = "block";
    else
        document.getElementById("last_updated_ts").style.display = "none";

    if (cmd == "create_token")
        document.getElementById("credential").style.display = "block";
    else
        document.getElementById("credential").style.display = "none";

    if ((cmd == "get_pkeys") || (cmd == "create_pub") || (cmd == "delete_pub"))
        document.getElementById("pub_id_text").style.display = "block";
    else
        document.getElementById("pub_id_text").style.display = "none";
    
    if (cmd == "revoke_token")
        document.getElementById("token_to_revoke").style.display = "block";
    else
        document.getElementById("token_to_revoke").style.display = "none";
}

function onLoad() {
    showControls();
}

function onChange() {
    showControls();
}

function onSubmit() {
    cmd = document.getElementById("command_list").value;
    if (cmd == "put_pkeys") {
        if ((document.getElementById("keys_to_upload").value.length <= 0) || (document.getElementById("pub_id").value.length <= 0)) {
            alert("Please make sure that you should enter both keys to upload and pub_id");
        }
    } else if (cmd == "get_pkeys") {
        if (document.getElementById("pub_id").value.length <= 0) {
            alert("Please make sure that you should enter pub_id");
        }
    }
}
</script>
<style>
p {
  display: block;
  margin-top: 0;
  margin-bottom: 0;
  margin-left: 1em;
  margin-right: 0;
}
</style>
</head>

<body onload="onLoad()">
<h2> Key Server Admin Page </h2>

<form action="/admin?token={{token}}" method="post" id="run_cmd" onsubmit="onSubmit()">
	Select a command to run : <select name="command_list" id="command_list" onchange="onChange()" form="run_cmd">
    <% for command in cmdList:
        if cmd and command == cmd:
    %>
            <option value="{{command}}" selected="selected">{{command}}</option>
        % else:
            <option value="{{command}}">{{command}}</option>
        % end
    % end
	</select><input type="submit" value="Run Command"><br>
    % if token:
    <p>- token : <input type="text" id="token" name="token" value="{{token}}"></p>
    % else:
    <p>- token : <input type="text" id="token" name="token"></p>
    % end
    % if token_revoke:
        <p id="token_to_revoke">- token_revoke : <input type="text" id="token_revoke" name="token_revoke" value="{{token_revoke}}"></p>
    % else:
        <p id="token_to_revoke">- token_revoke : <input type="text" id="token_revoke" name="token_revoke"></p>
    % end
    % if last_updated:
        <p id="last_updated_ts">- last_updated : <input type="text" id="last_updated" name="last_updated" value="{{last_updated}}"></p>
    % else:
        <p id="last_updated_ts">- last_updated : <input type="text" id="last_updated" name="last_updated"></p>
    % end
    <p id="credential">- role_id : 
    % if role_id:
        <input type="text" id="role_id" name="role_id" value="{{role_id}}><br>
    % else:
        <input type="text" id="role_id" name="role_id"><br>
    % end
    - secret_id : 
    % if role_id:
        <input type="text" id="secret_id" name="secret_id" value="{{secret_id}}><br>
    % else:
        <input type="text" id="secret_id" name="secret_id"><br>
    % end
    </p>
    
    % if pub_id:
	<p id="pub_id_text">- pub_id : <input type="number" id="pub_id" name="pub_id" value="{{pub_id}}"><br></p>
    % else:
	<p id="pub_id_text">- pub_id : <input type="number" id="pub_id" name="pub_id"><br></p>
    % end
    % if keys_to_upload:
    % rows = len(keys_to_upload) / 60
    <p id="upload_keys">- keys to upload : <textarea name="keys_to_upload" id="keys_to_upload" cols=80 rows={{rows}}>{{keys_to_upload}}</textarea></p>
    % else:
    <p id="upload_keys">- keys to upload : <textarea name="keys_to_upload" id="keys_to_upload" cols=80 rows=5></textarea></p>
    % end
</form>
% if cmd:
output : <embed src="/admin/output?token={{token}}" width="800" height="500"><br>
% end
</body>
</html>