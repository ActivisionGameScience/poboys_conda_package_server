<h1>{{header}}</h1>

%for f in filelist:
    %if allow_delete:
    <div>
        <form action="{{prefix}}/delete{{parenturl}}/{{f}}" method="post">
            <a href="{{prefix}}{{parenturl}}/{{f}}">{{f}}</a>
            <input type="submit" value="Delete" />
        </form>
    </div>
    %else:
    <div>
        <a href="{{prefix}}{{parenturl}}/{{f}}">{{f}}</a>
    </div>
    %end
%end
