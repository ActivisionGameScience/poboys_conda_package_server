<h1>Poboy's Conda Package Server</h1>

<h2>Browse</h2>
<a href="{{prefix}}/pkgs">Package list</a>

<h2>Upload</h2>
<form action="{{prefix}}/upload" method="post" enctype="multipart/form-data">
    <div>platform
        <select name="platform">
            %for platform in platforms:
            <option value="{{platform}}">{{platform}}</option>    
            %end 
        </select>
    </div>
    <div>filename
        <input type="file" name="fileupload" />
    </div>
    <div>
        <input type="submit" value="Upload" />
    </div>
</form>
