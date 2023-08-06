import plotly.graph_objects as go
import random
import teradataml as tdml
import io
from IPython.display import Image
import imageio
import matplotlib.pyplot as plt
import seaborn as sns

import random  # Importing the random module for random number generation

def colors(n, alpha=0.8, random_seed=124):
    """
    Generates a list of n colors in the form of RGBA strings.

    Parameters:
    - n (integer): The number of colors to generate.
    - alpha (float, optional): The alpha value (opacity) for each color. Defaults to 0.8.
    - random_seed (integer, optional): The seed value used for random number generation. Defaults to 124.

    Returns:
    - ret (list): A list of RGBA strings representing the generated colors.
    """

    random.seed(random_seed)  # Seed the random number generator for consistent colors

    ret = []  # Initialize an empty list to store the generated colors

    # Generate random values for the initial color components (r, g, b)
    r = int(random.random() * 256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)

    step = 256 / n  # Calculate the step interval between each color component

    # Generate n colors
    for i in range(n):
        r += step  # Increment the red component by the step interval
        g += step  # Increment the green component by the step interval
        b += step  # Increment the blue component by the step interval

        r = int(r) % 256  # Wrap around the red component to the range 0-255
        g = int(g) % 256  # Wrap around the green component to the range 0-255
        b = int(b) % 256  # Wrap around the blue component to the range 0-255

        # Construct the RGBA string and append it to the ret list
        ret.append("rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(alpha) + ")")

    return ret  # Return the list of generated colors



def plot_first_main_paths(myPathAnalysis, path_column='mypath', id_column='travelid', nb_paths=15, print_query=False,
                          font_size=10, width=1200, height=800, weight_column = None, weight_agg = 'count', justify='left'):
    """
        Plots the first main paths based on a given output of the teradataml NPATH function or the teradataml dataframe of its result field.

        Parameters:
        - myPathAnalysis (DataFrame or tdml.dataframe.dataframe.DataFrame): The input DataFrame containing path analysis data.
        - path_column (str, optional): The column name representing the path. Defaults to 'mypath'.
        - id_column (str or list, optional): The column name(s) representing the unique identifier(s). Defaults to 'travelid'.
        - nb_paths (int, optional): The number of main paths to plot. Defaults to 15.
        - print_query (bool, optional): Whether to print the generated query. Defaults to False.
        - font_size (int, optional): define the size of the font. Defaults is 10.
        - width (int, optional): define the width of the figure. Defaults is 1200.
        - height (int, optional): define the height of the figure. Defaults is 800.
        - weight_column (str, optional): define the column to aggregate. If None, just count the number of pathes.
          Default is None.
        - weight_agg (str, optional): when weight_column is not None, then the weight is the result of the aggregation
          defined by weight_agg on the weight_column. Permitted values are 'count', 'avg', 'max', 'min', 'sum'.
          Default is 'count'.
        - justify (str, optional): define if you want to justify 'right_(i)' (i=1,..,8) or 'left' or 'both' the output sankey. Defaults is 'left'.

        Returns:
        - None (it display an interactive Sankey plot)
    """
    if type(id_column) != list:
        id_column = [id_column]

    if weight_column == None:

        if type(myPathAnalysis) != tdml.dataframe.dataframe.DataFrame:
            df_agg = myPathAnalysis.result.select(id_column+[path_column]).groupby(path_column).count()
        else:
            df_agg = myPathAnalysis.select(id_column+[path_column]).groupby(path_column).count()

        df_agg._DataFrame__execute_node_and_set_table_name(df_agg._nodeid, df_agg._metaexpr)

        query = f"""SEL
            row_number() OVER (PARTITION BY 1 ORDER BY count_{id_column[0]} DESC) as id
        ,	REGEXP_REPLACE(lower(A.{path_column}),'\\[|\\]', '') as str
        ,	count_{id_column[0]} as weight
        FROM {df_agg._table_name} A
        QUALIFY id < {nb_paths}+1"""

    else:
        if type(myPathAnalysis) != tdml.dataframe.dataframe.DataFrame:
            df_agg = myPathAnalysis.result.select(list(set(id_column + [path_column] + [weight_column]))).groupby(path_column).agg({weight_column : weight_agg})
        else:
            df_agg = myPathAnalysis.select(list(set(id_column + [path_column] + [weight_column]))).groupby(path_column).agg({weight_column : weight_agg})

        df_agg._DataFrame__execute_node_and_set_table_name(df_agg._nodeid, df_agg._metaexpr)

        query = f"""SEL
            row_number() OVER (PARTITION BY 1 ORDER BY {weight_agg}_{weight_column} DESC) as id
        ,	REGEXP_REPLACE(lower(A.{path_column}),'\\[|\\]', '') as str
        ,	{weight_agg}_{weight_column} as weight
        FROM {df_agg._table_name} A
        QUALIFY id < {nb_paths}+1"""

    df_selection = tdml.DataFrame.from_query(query)

    if justify == 'left':
        justify_query = 'AAA.id_end_temp AS id_end'
        ascending     = ''
        init          = '0'
    elif justify == 'right':
        justify_query = '''max_max_path_length - AAA.id_end_temp as id_end'''
        ascending     = ' DESC'
        init          = 'max_path_length'
    elif justify == 'both':
        justify_query = '''AAA.id_end_temp as id_end'''
        ascending     = ' DESC'
        init          = '0'

    query2 = f"""
    sel
        CC.id
    ,   CC.node_source
    ,	CC.node_target
    ,	CC.beg
    ,	CC."end"
    ,	sum(CC.weight) as weight
    FROM 
    (
    sel
        B.*
    ,	LAG(id_end,1,{init}) OVER (PARTITION BY B."path" ORDER BY B."index" ) as id_beg
    ,	B."beg" || '_' || TRIM(CAST(id_beg AS VARCHAR(200))) as node_source
    ,	B."end" || '_' || TRIM(CAST(id_end AS VARCHAR(200))) as node_target
    FROM 
    (
        SEL
            AAA.*
        ,   {justify_query}
        ,   MAX(AAA.id_end_temp) OVER (PARTITION BY AAA."path") AS max_path_length
        ,   MAX(AAA.id_end_temp) OVER (PARTITION BY 1) AS max_max_path_length
        FROM (
            sel 
                A.*
            ,	row_number() OVER (PARTITION BY A."path" ORDER BY A."index" {ascending}) as id_end_temp
            from (
                SELECT
        
                    lag(AA.token,1) IGNORE NULLS OVER (PARTITION BY AA.outkey ORDER BY AA.tokennum) as "beg"
                ,	AA.token as "end"
                ,	AA.outkey as "path"
                ,	B.weight
                ,	AA.tokennum as "index"
                ,   B.id
                FROM (
        
                    SELECT 
                        d.*
                    FROM TABLE (strtok_split_to_table({df_selection._table_name}.id, {df_selection._table_name}.str, ',')
                    RETURNS (outkey integer, tokennum integer, token varchar(200)character set unicode) ) as d 
            
                    ) AA
                ,{df_selection._table_name} B
                WHERE AA.outkey = B.id
                QUALIFY beg IS NOT NULL
            ) A
        ) AAA
    ) B
    --ORDER BY "path","index"
    ) CC
    GROUP BY 1,2,3,4,5
    """

    if print_query:
        print(query2)

    df_ready = tdml.DataFrame.from_query(query2)

    df_ready_local = df_ready.to_pandas()

    df_ready_local = df_ready_local.sort_values(by=['id','node_source','node_target'])

    labs = dict()
    labels = list(set(df_ready_local.node_source.tolist() + df_ready_local.node_target.tolist()))

    for i, label in enumerate(labels):
        labs[label] = i

    labels = ['_'.join(x.split('_')[0:(len(x.split('_')) - 1)]) for x in labels]

    df_ready_local['color'] = df_ready_local.id.map(
        {id: col for id, col in zip(list(set(df_ready_local.id)), colors(len(set(df_ready_local.id)), random_seed=45))})

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=colors(len(labels), random_seed=123)
        ),
        link=dict(
            source=df_ready_local.node_source.map(labs),  # indices correspond to labels, eg A1, A2, A2, B1, ...
            target=df_ready_local.node_target.map(labs),
            value=df_ready_local.weight,
            color=df_ready_local.color
        ))])

    fig.update_layout(font_size=font_size, width=width,
                      height=height)
    fig.show()

    return

def create_all_pathes_views(myPathAnalysis, root_name = 'mytest',
                            schema = tdml.get_context().execute('SELECT DATABASE').fetchall()[0][0],
                            path_column='mypath', id_column='travelid', justify = 'left'):
    """
        Creates multiple views related to the given myPathAnalysis DataFrame.

        Parameters:
        - myPathAnalysis (DataFrame or tdml.dataframe.dataframe.DataFrame): The input DataFrame containing path analysis data.
        - root_name (str, optional): The root name to be used for naming the created views. Defaults to 'mytest'.
        - schema (str, optional): The schema to create the views in. Defaults to the current database schema.
        - path_column (str, optional): The column name representing the path. Defaults to 'mypath'.
        - id_column (str or list, optional): The column name(s) representing the unique identifier(s). Defaults to 'travelid'.
        - justify (str, optional): define if you want to justify 'right' or 'left' or 'both' the output sankey. Defaults is 'left'.

        Returns:
        - None
    """

    if type(id_column) != list:
        id_column = [id_column]

    # Create the view of my npath
    npath_view = f"{schema}.{root_name}_NPATH_VIEW"

    try:
        query = f"""
        REPLACE VIEW  {npath_view} AS
        {myPathAnalysis.sqlmr_query}
        """
    except Exception as e:
        print(str(e).split('\n')[0])
        query = f"""
        REPLACE VIEW  {npath_view} AS
        {myPathAnalysis.show_query()}
        """
    tdml.get_context().execute(query)
    print(f'npath view created : {npath_view}')

    # Create the aggregated view of my npath
    aggregated_npath_view = f"{schema}.{root_name}_NPATH_VIEW_AGG"
    query = f"""
    REPLACE VIEW {aggregated_npath_view} AS
    SELECT 
        {path_column}
    ,   COUNT(*) as count_{id_column[0]}
    FROM {npath_view}
    GROUP BY 1
    """
    tdml.get_context().execute(query)
    print(f'aggregated npath view created : {aggregated_npath_view}')

    # Create the cleaned aggregated view of my npath
    clean_aggregated_npath_view = f"{schema}.{root_name}_CLEAN_NPATH_VIEW_AGG"
    query = f"""
    REPLACE VIEW {clean_aggregated_npath_view} AS
    SELECT 
        row_number() OVER (PARTITION BY 1 ORDER BY count_{id_column[0]} DESC) as id
    ,	REGEXP_REPLACE(lower(A.{path_column}),'\[|\]', '') as str
    ,	count_{id_column[0]} as weight
    FROM {aggregated_npath_view} A"""
    tdml.get_context().execute(query)
    print(f'clean aggregated npath view created : {clean_aggregated_npath_view}')

    if justify == 'left':
        justify_query = 'AAA.id_end_temp AS id_end'
        ascending     = ''
        init          = '0'
    elif justify == 'right':
        justify_query = '''max_max_path_length - AAA.id_end_temp as id_end'''
        ascending     = ' DESC'
        init          = 'max_path_length'
    elif justify == 'both':
        justify_query = '''AAA.id_end_temp as id_end'''
        ascending     = ' DESC'
        init          = '0'

    # Create the graph view of the aggregated npath view
    graph_aggregated_npath_view =  f"{schema}.{root_name}_GRAPH_NPATH_VIEW_AGG"
    query = f"""
    REPLACE VIEW {graph_aggregated_npath_view} AS
    SELECT
        CC.id
    ,	CC.node_source
    ,	CC.node_target
    ,	CC.beg
    ,	CC."end"
    ,	sum(CC.weight) as weight
    FROM 
    (
    sel
        B.*
    ,	LAG(id_end,1,{init}) OVER (PARTITION BY B."path" ORDER BY B."index" ) as id_beg
    ,	B."beg" || '_' || TRIM(CAST(id_beg AS VARCHAR(10))) as node_source
    ,	B."end" || '_' || TRIM(CAST(id_end AS VARCHAR(10))) as node_target
    FROM 
        (
        SEL
            AAA.*
        ,   {justify_query}
        ,   MAX(AAA.id_end_temp) OVER (PARTITION BY AAA."path") AS max_path_length
        ,   MAX(AAA.id_end_temp) OVER (PARTITION BY 1) AS max_max_path_length
        FROM (
            sel 
                A.*
            ,	row_number() OVER (PARTITION BY A."path" ORDER BY A."index" {ascending}) as id_end_temp
            from (
                SELECT
        
                    lag(AA.token,1) IGNORE NULLS OVER (PARTITION BY AA.outkey ORDER BY AA.tokennum) as "beg"
                ,	AA.token as "end"
                ,	AA.outkey as "path"
                ,	B.weight
                ,	AA.tokennum as "index"
                ,   B.id
                FROM (
                    SELECT 
                        d.*
                    FROM TABLE (strtok_split_to_table({clean_aggregated_npath_view}.id, {clean_aggregated_npath_view}.str, ',')
                    RETURNS (outkey integer, tokennum integer, token varchar(20)character set unicode) ) as d 
                ) AA
                ,   {clean_aggregated_npath_view} B
                WHERE AA.outkey = B.id
                QUALIFY beg IS NOT NULL
            ) A
        ) AAA
       ) B
    --ORDER BY "path","index"
    ) CC
    GROUP BY 1,2,3,4,5
    """
    tdml.get_context().execute(query)
    print(f'npath view created : {graph_aggregated_npath_view}')

    return





def scatter_plot(tddf, x_col, y_col, **kwargs):
    """
    This function generates a scatter plot based on the given parameters.
    This function used TD_PLOT so requires Teradata 17.20 or later versions.

    Parameters
    ----------
    tddf : teradata DataFrame
        The DataFrame from which the plot will be generated.
    x_col : str
        The column of the DataFrame to use as the x-axis.
    y_col : str
        The column of the DataFrame to use as the y-axis.
    **kwargs :
        Additional optional parameters can be set as follows:

        width : int, optional
            The width of the plot, defaults to 600.
        height : int, optional
            The height of the plot, defaults to 600.
        row_axis_type : str, optional
            The type of axis, defaults to 'SEQUENCE'.
        series_id : str or list, optional
            The id(s) of the series, defaults to None.
        color : str, optional
            The color of the marker, defaults to 'b'.
        marker : str, optional
            The shape of the marker, defaults to 'o'.
        markersize : int, optional
            The size of the marker, defaults to 3.
        noplot : bool, optional
            If True, the plot will not be displayed, defaults to False.
        title : str, optional
            The title of the plot, defaults to '{y_col} Vs. {x_col}'.

    Returns
    -------
    Image
        either the image read from the stream or the Image object object containing the scatter plot (depending on the "no_plot" option).
    """

    # Fetch keyword arguments with default values
    width = kwargs.get('width', 600)
    height = kwargs.get('height', 600)
    row_axis_type = kwargs.get('row_axis_type', 'SEQUENCE')
    series_id = kwargs.get('series_id', None)
    color = kwargs.get('color', 'b')
    marker = kwargs.get('marker', 'o')
    markersize = kwargs.get('markersize', 3)
    noplot = kwargs.get('noplot', False)
    title = kwargs.get('title', f'{y_col} Vs. {x_col}')

    # If no series id is provided, a default one is created
    if series_id is None:
        tddf = tddf.assign(series_id=1)
        series_id = 'series_id'

    n = 1
    # If series_id is a list, its length is stored and it's joined into a comma-separated string
    if type(series_id) == list:
        n = len(series_id)
        series_id = ','.join(series_id)

    # This line is specific to teradata DataFrame structure,
    # it aims to be sure the name of the temporary view is available
    tddf._DataFrame__execute_node_and_set_table_name(tddf._nodeid, tddf._metaexpr)

    # SQL query to be executed using TD_PLOT
    query = f"""
    EXECUTE FUNCTION
        TD_PLOT(
            SERIES_SPEC(
            TABLE_NAME({tddf._table_name}),
            ROW_AXIS({row_axis_type}({x_col})),
            SERIES_ID({series_id}),
            PAYLOAD (
                FIELDS({y_col}),
                CONTENT(REAL)
            )
        ),
        FUNC_PARAMS(
        TITLE('{title}'),
        PLOTS[(
        TYPE('scatter'),
        MARKER('{marker}'),
        MARKERSIZE({markersize})
        --COLOR('{color}')
        )],
        WIDTH({width}),
        HEIGHT({height})
        )
        );
    """

    # If enabled, print the SQL query
    if tdml.display.print_sqlmr_query:
        print(query)

    # Execute the query and fetch the result
    res = tdml.get_context().execute(query).fetchall()

    stream_str = io.BytesIO(res[0][1 + n])

    # Return either the image read from the stream or the Image object
    if noplot:
        return imageio.imread(stream_str.getvalue())
    else:
        return Image(stream_str.getvalue())


def pair_plot(tddf, **kwargs):
    """
    This function generates a pair plot based on the given parameters.
    This function used TD_PLOT so requires Teradata 17.20 or later versions.

    Parameters
    ----------
    tddf : teradata DataFrame
        The DataFrame from which the plot will be generated.
    **kwargs :
        Additional optional parameters can be set as follows:

        width : int, optional
            The width of the plot, defaults to 600.
        height : int, optional
            The height of the plot, defaults to 600.
        row_axis_type : str, optional
            The type of axis, defaults to 'SEQUENCE'.
        series_id : str or list, optional
            The id(s) of the series, defaults to None.
        color : str, optional
            The color of the marker, defaults to 'b'.
        marker : str, optional
            The shape of the marker, defaults to 'o'.
        noplot : bool, optional
            If True, the plot will not be displayed, defaults to False.
        title : str, optional
            The title of the plot, defaults to 'pairplot'.
        markersize : int, optional
            The size of the marker, defaults to 3.

    Returns
    -------
    Image
        An Image object containing the pair plot.
    """

    # Fetch keyword arguments with default values
    width = kwargs.get('width', 600)
    height = kwargs.get('height', 600)
    row_axis_type = kwargs.get('row_axis_type', 'SEQUENCE')
    series_id = kwargs.get('series_id', None)
    color = kwargs.get('color', 'b')
    marker = kwargs.get('marker', 'o')
    noplot = kwargs.get('noplot', False)
    title = kwargs.get('title', 'pairplot')
    markersize = kwargs.get('markersize', 3)

    # If no series id is provided, a default one is created
    if series_id is None:
        tddf = tddf.assign(series_id=1)
        series_id = 'series_id'

    n = 1
    # If series_id is a list, its length is stored and it's joined into a comma-separated string
    if type(series_id) == list:
        n = len(series_id)
        series_id = ','.join(series_id)

    # This line is specific to teradata DataFrame structure,
    # it aims to be sure the name of the temporary view is available
    tddf._DataFrame__execute_node_and_set_table_name(tddf._nodeid, tddf._metaexpr)

    # Determine which columns to include in the plot
    if type(series_id) == list:
        columns = [c for c in list(tddf.columns) if c not in series_id]
    else:
        columns = [c for c in list(tddf.columns) if c not in [series_id]]

    series_blocks = []
    plot_blocks = []
    counter = 0

    # For each pair of columns, add a block to the series_blocks and plot_blocks lists
    for i, c_row in enumerate(columns):
        for j, c_col in enumerate(columns):
            if i < j:
                counter += 1
                # Series block for the SQL query
                series_block = f"""
                SERIES_SPEC(
                TABLE_NAME({tddf._table_name}),
                ROW_AXIS({row_axis_type}({c_row})),
                SERIES_ID({series_id}),
                PAYLOAD (
                    FIELDS({c_col}),
                    CONTENT(REAL)
                ))"""
                series_blocks.append(series_block)

                # Plot block for the SQL query
                plot_block = f"""
                (
                    ID({counter}),
                    CELL({i + 1},{j}),
                    TYPE('scatter'),
                    MARKER('{marker}'),
                    MARKERSIZE({markersize})
                    --COLOR('{color}')
                    )
                """
                plot_blocks.append(plot_block)

    series_blocks = ',\n'.join(series_blocks)
    plot_blocks = ',\n'.join(plot_blocks)

    # SQL query to be executed
    query = f"""
    EXECUTE FUNCTION
        TD_PLOT(
            {series_blocks}
        ,
        FUNC_PARAMS(
        LAYOUT({len(columns) - 1},{len(columns) - 1}),
        TITLE('{title}'),
        WIDTH({width}),
        HEIGHT({height}),
        PLOTS[
            {plot_blocks}
        ]
        )
        );
    """

    # If enabled, print the SQL query
    if tdml.display.print_sqlmr_query:
        print(query)

    # Execute the query and fetch the result
    res = tdml.get_context().execute(query).fetchall()

    stream_str = io.BytesIO(res[0][1 + n])

    # Return either the image read from the stream or the Image object
    if noplot:
        return imageio.imread(stream_str.getvalue())
    else:
        return Image(stream_str.getvalue())


def plot_correlation_heatmap(tddf, **kwargs):
    """
    This function calculates the correlation matrix of a DataFrame and plots a heatmap of it.
    It requires Vantage Analytic Library installed with the rights to execute its functions.

    Parameters
    ----------
    tddf : teradata DataFrame
        The DataFrame for which the correlation matrix will be calculated and plotted.
    **kwargs :
        Additional optional parameters can be set as follows:

        ax : matplotlib axis, optional
            The axis on which the plot will be displayed. If none is given, the current axis will be used. Defaults to None.
        no_plot : bool, optional
            If True, the plot will not be displayed, and the function will return the correlation matrix. Defaults to False.
        title : str, optional
            The title of the plot, defaults to an empty string.

    Returns
    -------
    DataFrame or None
        If no_plot is True, a DataFrame containing the correlation matrix is returned.
        Otherwise, None is returned, and a heatmap of the correlation matrix is plotted.
    """

    # Fetch keyword arguments with default values
    ax = kwargs.get('ax', None)
    no_plot = kwargs.get('no_plot', False)
    title = kwargs.get('title', '')

    # compute the correlation matrix in-db
    obj = tdml.valib.Matrix(data=tddf,
                       columns=list(tddf.columns),
                       type="COR")

    # download the result
    val_corr_matrix = obj.result.to_pandas().reset_index().drop('rownum', axis=1).set_index('rowname').loc[
                      list(tddf.columns), :]

    # plot the heatmap
    if no_plot:
        return val_corr_matrix
    else:
        if ax != None:
            sns.heatmap(val_corr_matrix, annot=True, cmap='coolwarm', ax=ax)
            ax.set_title(title)
        else:
            sns.heatmap(val_corr_matrix, annot=True, cmap='coolwarm')
            plt.title(title)
