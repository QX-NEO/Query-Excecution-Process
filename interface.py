import streamlit as st
import preprocessing
import time



def main_interface():
    status,login = sidebar()
    if not status:
        st.error("Unable to connect")
    else:
        st.success("connection_succesful")
        query_example = example_query()
        if query_example:
            query_string  = read_query(query_example)
        else :
            query_string = write_query()

        try:
            table = preprocessing.read_query(query_string, login)
            st.dataframe(table)

        except:
            st.error("Unable to read query")



def sidebar():
    st.title("Welcome to Query Plan")
    st.sidebar.title(" Establish Connection")
    st.sidebar.markdown("## Database Name")
    dbname = st.sidebar.text_input("input database name")
    st.sidebar.markdown("## Username ")
    username = st.sidebar.text_input("input username")
    st.sidebar.markdown("## Password")
    password = st.sidebar.text_input("input password",type="password")
    st.sidebar.markdown("## Host ")
    host = st.sidebar.text_input("input host")
    st.sidebar.markdown("## Port ")
    port = st.sidebar.text_input("input port")

    login  = preprocessing.Authentication(dbname, username, password, host, port)
    connection_status = preprocessing.connect_sql(login)
    return connection_status, login



def example_query():
    st.subheader("Input Query:")
    example_query = ''

    if st.button('Example 1'):
        example_query = """select c_name , c_acctbal ,c_custkey, o_totalprice
                            from customer as a
                            join public.orders as b on a.c_custkey = b.o_custkey
                            where o_totalprice < 50000
                        """

    if st.button('Example 2'):
        example_query = """ SELECT
                            l_orderkey,
                            sum(l_extendedprice * (1 - l_discount)) as revenue,
                            o_orderdate,
                            o_shippriority
                        FROM
                            customer,
                            orders,
                            lineitem
                        WHERE
                            c_mktsegment = 'BUILDING'
                            AND c_custkey = o_custkey
                            AND l_orderkey = o_orderkey
                            AND o_orderdate < date '1995-03-15'
                            AND l_shipdate > date '1995-03-15'
                        GROUP BY
                            l_orderkey,
                            o_orderdate,
                            o_shippriority
                        ORDER BY
                            revenue desc,
                            o_orderdate
                        LIMIT 20;
                        """
    if st.button('Example 3'):
        example_query = """ SELECT
                                l_shipmode,
                                sum(case
                                    when o_orderpriority = '1-URGENT'
                                        OR o_orderpriority = '2-HIGH'
                                        then 1
                                    else 0
                                end) as high_line_count,
                                sum(case
                                    when o_orderpriority <> '1-URGENT'
                                        AND o_orderpriority <> '2-HIGH'
                                        then 1
                                    else 0
                                end) AS low_line_count
                            FROM
                                orders,
                                lineitem
                            WHERE
                                o_orderkey = l_orderkey
                                AND l_shipmode in ('MAIL', 'SHIP')
                                AND l_commitdate < l_receiptdate
                                AND l_shipdate < l_commitdate
                                AND l_receiptdate >= date '1994-01-01'
                                AND l_receiptdate < date '1994-01-01' + interval '1' year
                            GROUP BY
                                l_shipmode
                            ORDER BY
                                l_shipmode;
                        """
    return example_query


def read_query(example):
    query =  st.text_area("", example, height= 400, key = 'first', on_change=update_first)
    return query

def update_first():
    st.session_state.second = st.session_state.first

def update_second():
    st.session_state.first = st.session_state.second

def write_query():
     query =  st.text_area("", key = 'second', height= 400, on_change=update_second)
     return query 