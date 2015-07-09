<h1>{{header}}</h1>

%for f in dirlist:
    %if allow_delete:
    <div>
        <form action="/delete{{parentdir}}/{{f}}" method="post">
            <a href="{{parentdir}}/{{f}}">{{f}}</a>
            <input type="submit" value="Delete" />
        </form>
    </div>
    %else:
    <div>
        <a href="{{parentdir}}/{{f}}">{{f}}</a>
    </div>
    %end
%end
