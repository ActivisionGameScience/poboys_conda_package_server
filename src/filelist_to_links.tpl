<h1>{{header}}</h1>

%for f in filelist:
    %if allow_delete:
    <div>
        <form action="/delete{{parenturl}}/{{f}}" method="post">
            <a href="{{parenturl}}/{{f}}">{{f}}</a>
            <input type="submit" value="Delete" />
        </form>
    </div>
    %else:
    <div>
        <a href="{{parenturl}}/{{f}}">{{f}}</a>
    </div>
    %end
%end
