import numpy as np
import scipy.optimize as op
import scipy.special as fn
import pylab as p
import math

fwhm_coef=2.*math.sqrt(2.*math.log(2.))
sqrt_2pi=math.sqrt(2.*math.pi)
sqrt_2 = math.sqrt(2.)

def gauss(x, x0, A, fwhm):
    sigma = fwhm/fwhm_coef
    _c=A  #/(sigma*sqrt_2pi)
    _=((x-x0)**2)/(2*sigma**2)
    # print _, _c
    _=np.exp(-_)*_c
    return _

def test1():
    channels=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,3,5,8,19,     37,57,110,201,331,602,1006,1683
,2646,4283,6783,10382,15344,22612,32871,     45971,63336,85157,112676,144016,183174,226837,
275037,324926,376696,428399,     474959,515910,548642,570915,581400,579176,565419,538934,505254,
461770,     414213,363708,312642,263381,217939,176157,139385,108892,83128,61869,45213,     32574
,22949,15943,10889,7380,4810,3253,2117,1347,976,638,418,323,204,188,     159,141,97,94,83,90,75
,74,70,57,62,63,75,55,64,34,29,36,27,21,22,16,12,     27,41,37,45,49,37,49,49,84,80,90,154,293
,638,1374,2277,3247,3821,4012,     3927,3855,3869,3845,3804,3830,3664,3667,3777,3823,3753,3643,
3558,3614,     3482,3457,3609,3542,3428,3452,3319,3393,3426,3346,3229,3312,3223,3258,     3243,
3193,3122,3092,3230,3150,3078,3121,3066,3194,3085,3033,3103,2919,     2902,3038,3121,2866,2951,
2906,2888,2983,2882,2850,2894,2940,2882,2842,     2771,2862,2847,2851,2859,2816,2766,2714,2831,
2719,2757,2810,2723,2713,     2657,2700,2725,2802,2684,2695,2691,2680,2694,2702,2638,2686,2588,
2609,     2653,2534,2605,2608,2579,2569,2624,2622,2525,2580,2578,2565,2640,2614,     2558,2562,
2516,2575,2538,2565,2514,2427,2574,2534,2582,2435,2421,2579,     2456,2484,2436,2384,2562,2390,
2411,2444,2414,2437,2317,2429,2376,2413,     2347,2330,2389,2431,2381,2371,2345,2399,2362,2460,
2423,2322,2348,2318,     2277,2258,2257,2215,2291,2310,2136,2279,2100,2125,2165,2155,2110,2061,
     2127,2053,2035,2051,2075,1964,1962,1962,2028,2025,2086,2030,2058,1953,     1992,1970,2053,
2030,2018,1982,2048,2051,1915,2005,2011,2024,2035,1983,     1984,2011,1927,1928,1962,1982,1933,
1822,1908,1869,1891,1980,1897,1892,     1913,1849,2019,2038,2081,2052,2201,2292,2449,2722,2848,
3087,3435,3739,     4232,4698,5115,5805,6294,6984,7817,8285,9215,9612,10265,10762,11107,
11397,11539,11585,11485,11413,11112,10818,10480,9978,9461,8814,8145,     7864,7261,7063,6597,
6120,5824,5501,5286,5048,4717,4667,4578,4489,4594,     4638,4889,5255,5841,6563,7533,8858,10589
,12603,15007,17943,21444,25399,     29728,34756,40006,45571,51301,56779,62070,67589,72754,77015,
80603,82682,     83931,84935,84480,83473,80914,77332,73071,68805,63644,58770,53293,47728,
42893,37443,32859,29090,25032,22040,18677,16320,14142,12538,10814,9553,     8635,7719,6851,6180,
5835,5144,4935,4759,4436,4241,4113,3948,4005,3913,     3876,3797,3739,3767,3746,3762,3551,3646,
3547,3552,3496,3476,3302,3230,     3143,3133,2981,2872,2830,2718,2697,2707,2492,2549,2441,2362,
2282,2237,     2150,2214,2086,2133,1993,1999,2019,1955,1828,1880,1848,1889,1825,1883,     1840,
1755,1718,1822,1646,1756,1788,1737,1732,1629,1682,1631,1706,1722,     1728,1748,1739,1663,1766,
1756,1761,1682,1812,1765,1754,1874,1809,1825,     1755,1824,1843,1808,1754,1774,1750,1766,1903,
1796,1740,1708,1717,1701,     1639,1704,1752,1712,1602,1701,1614,1631,1661,1633,1677,1625,1581,
1623,     1617,1625,1636,1582,1600,1628,1625,1589,1580,1648,1583,1564,1592,1519,     1599,1657,
1596,1598,1567,1633,1688,1656,1588,1591,1589,1701,1694,1735,     1682,1723,1701,1751,1809,1910,
1847,1838,1926,1890,1966,1998,2019,2017,     1901,2024,1983,1968,1966,1956,1939,1928,1937,1984,
1900,1832,1899,1956,     1924,1836,1903,1946,1973,1957,1953,2051,1960,1953,2019,1977,1964,2016,
     1947,1995,2019,1979,2012,1960,2056,1962,1963,1986,1995,1921,1936,1879,     1827,1871,1899,
1880,1899,1809,1919,1848,1877,1852,1876,1909,1910,1929,     2086,1992,2188,2146,2142,2131,2084,
2225,2147,2127,2219,2271,2259,2285,     2263,2204,2168,2115,2151,2159,2094,2103,1994,2014,1948,
1971,2018,1952,     1917,2014,1963,2021,1857,1999,1982,2018,2012,2059,2069,2099,2137,2173,
2181,2214,2364,2442,2522,2616,2822,3152,3353,3737,4123,4704,5483,6301,     7434,8758,10371,
12037,14287,16829,20204,23741,27753,32321,37330,42397,     48679,54519,61426,68407,75284,81925,
88818,95139,101377,106392,110984,     114684,117829,119732,119976,119714,118406,115420,111845,
107262,101514,     96162,89506,83032,75387,69004,62465,54984,48873,42564,37661,31846,27707,
23633,20132,17132,14310,12154,10238,8846,7672,6659,5952,5450,5033,4894,     4779,4965,5148,5457
,5838,6236,6847,7528,8474,9119,10153,11196,12524,     13895,15265,16646,18467,20479,22489,24838
,27217,30123,33336,36433,40748,     44573,49188,53508,59492,64830,71255,77696,83567,90527,97050,
103143,109422,     114846,120182,124433,128548,130701,132814,132637,132333,131539,128022,
124166,119944,115248,108549,101801,95079,87876,80181,72321,65021,58187,     51734,45219,39529,
34086,29596,25072,21297,17662,15030,12621,10451,8765,     7566,6296,5375,4622,3994,3623,3338,
3168,3019,2963,3065,3061,3299,3614,     3563,4076,4381,4782,5202,5783,6457,7147,7807,8476,9415,
10250,10991,11957,     12926,13833,14615,15297,16154,16808,17560,17770,18109,18157,18342,18451,
     17854,17837,17078,16610,16147,15275,14054,13365,12629,11398,10717,10014,     8846,8031,7190
,6487,5882,5208,4515,4210,3690,3267,3008,2713,2427,2226,     2044,1878,1757,1706,1597,1592,1521
,1412,1429,1346,1407,1385,1386,1342,     1365,1366,1425,1428,1387,1304,1392,1435,1334,1401,1494
,1437,1499,1515,     1470,1614,1695,1641,1691,1871,1912,2067,2213,2426,2634,2889,3154,3545,
     3960,4579,5048,5854,6645,7437,8680,9697,11061,12439,14091,16037,17444,     19398,21623,
23682,25559,27680,29667,32011,34128,35834,37527,38856,41119,     41379,42055,42299,42951,42888,
41962,41292,40570,39615,37550,35993,34197,     32387,30324,28645,26050,24065,22446,20491,18664,
16961,15249,14004,12634,     11437,10615,9996,9112,8449,7884,7353,7042,6515,6412,6093,5831,5566
,5308,     5070,4736,4743,4598,4263,4308,4015,3929,3800,3844,3741,3733,3758,3756,     3819,3978
,4098,4173,4423,4591,4890,5124,5170,5433,5749,6002,6119,6402,     6752,6838,7150,7315,7697,7683
,8210,8194,8411,8418,8766,8755,8824,9316,     9391,9347,9663,9494,9572,9470,9577,9397,9381,8930
,8790,8799,8545,8386,     8006,7676,7159,6827,6554,6221,5768,5499,5247,4806,4479,4209,3781,3715
,     3446,3173,3018,2771,2597,2511,2421,2384,2297,2258,2187,2219,2233,2229,     2210,2203,2221
,2302,2352,2320,2377,2456,2433,2433,2500,2449,2502,2451,     2506,2502,2564,2481,2521,2549,2502
,2345,2457,2409,2432,2319,2413,2218,     2358,2323,2344,2320,2308,2352,2248,2337,2265,2180,2297
,2184,2071,2223,     2235,2169,2166,2136,2242,2150,2104,2083,2100,2124,2081,2057,2130,2063,
     2082,2040,1999,2038,1963,2018,2006,1880,2029,2033,2178,2015,2119,2073,     2096,2136,2114,
2096,2105,2176,2175,2161,2124,2222,2210,2150,2301,2229,     2331,2208,2278,2300,2268,2214,2138,
2254,2273,2185,2131,2125,2050,2060,     2125,1969,2036,2042,2026,1951,1913,1904,1956,1870,1884,
1906,1785,1907,     1943,1892,1781,1882,1964,2067,1947,2009,2076,2185,2216,2212,2284,2349,
2535,2660,2885,2966,3042,3428,3490,3972,4168,4674,4979,5325,5888,6334,     6893,7398,8138,8778,
9488,10231,11096,11595,12222,12856,13790,14385,14831,     15384,15922,16191,16514,16603,16918,
16960,16844,16634,16216,16028,15739,     15095,14406,14047,13017,12704,11662,11099,10368,9813,
8930,8418,7758,7305,     6841,6249,5924,5398,5062,4769,4467,4293,4189,3985,3846,3609,3629,3649,
     3554,3495,3529,3481,3593,3542,3555,3665,3704,3833,3966,3926,4121,4248,     4307,4378,4631,
4886,5101,5375,5707,5996,6390,7071,7483,8226,9117,10424,     11884,13838,15550,18256,21663,
25321,29942,34933,41444,49066,57880,68104,     79097,93206,108467,125905,145302,167334,190234,
215787,243561,273199,     305256,338845,374630,410922,447619,483237,521626,558315,594427,626179,
     658777,687807,714286,735083,753942,768135,775673,779820,776828,774598,     761417,747270,
727100,702896,676692,648849,613594,582254,544090,508350,     471945,433457,396586,361645,326468,
292739,260941,232228,205463,179433,     157424,136009,118031,101327,86412,73683,61835,52204,
44458,36845,31104,     25587,21165,17464,14641,12186,10135,8603,7178,6219,5488,4783,4156,3760,
     3399,3246,3044,2841,2722,2618,2622,2597,2415,2371,2343,2358,2337,2420,     2323,2244,2332,
2318,2252,2318,2318,2331,2373,2427,2365,2428,2423,2441,     2590,2601,2564,2652,2751,2826,2836,
2938,3091,3157,3261,3491,3692,3802,     4038,4317,4604,4881,5410,5745,6143,6805,7512,8415,9355,
10347,11487,13033,     14368,16448,18217,20398,22655,25103,27986,31235,34530,38595,42181,46464,
     50155,54478,59007,63727,68130,72736,77388,81520,85569,88531,92392,94732,     97444,99007,
101002,102329,102220,101955,101542,99811,98312,95524,92644,     89335,85911,81682,77613,73085,
68070,63993,58972,54656,50349,45765,41363,     37333,34125,29786,26653,23578,20667,18214,15789,
13963,11999,10409,8899,     7752,6463,5482,4735,4054,3477,2969,2463,2253,1836,1577,1363,1231,
1061,     997,925,874,761,739,692,665,649,605,636,558,552,591,595,558,562,562,     543,563,536,
526,572,571,593,581,580,547,539,561,541,578,586,550,561,     541,574,542,539,507,539,591,489,
506,517,476,493,462,486,454,454,465,     423,441,436,444,440,412,384,444,416,421,400,419,371,
390,384,433,404,     447,403,429,372,382,422,396,417,438,448,421,421,393,425,392,382,374,
398,409,389,413,409,406,442,424,441,398,417,379,445,435,436,463,418,     446,421,469,457,505,
470,477,477,495,470,463,538,511,574,526,526,491,     588,585,557,591,615,602,656,628,698,708,
714,765,793,844,862,898,932,     1024,1049,1102,1170,1147,1234,1273,1323,1348,1379,1403,1517,
1569,1495,     1598,1600,1607,1582,1629,1679,1635,1680,1652,1589,1547,1512,1491,1518,     1482,
1339,1363,1321,1275,1237,1203,1149,1079,1046,995,986,935,972,844,     811,821,750,755,770,729,
640,578,600,604,541,542,483,498,483,477,445,488,     414,451,426,432,399,401,408,424,405,368,
425,417,374,393,389,376,380,413,     387,400,413,404,400,413,393,420,403,389,432,441,403,412,
430,449,429,462,     508,487,482,566,510,589,635,679,688,788,847,900,954,1074,1108,1254,1349,
     1437,1507,1667,1778,1869,2021,2163,2177,2436,2500,2611,2746,2860,2917,3023,3010,3066,3192,
 3207,3223,3239,3238,3191,3092,3063,3042,3005,2781,2819,2645,2469,2453,2375,2175,2103,2022,1891
, 1805,1649,1514,1454,1303,1287,1120,1026,1033,963,902,806,756,695,614,681,610,610,536,603,557,
 537,483,502,493,505,492,493,487,552,478,500,520,471,501,533,578,508,528,497,501,492,487,478,
476 ,497,460,494,467,488,470,471,453,447,453,427,452,478,469,434,463,429,378,434,470,430,403,
470, 456,441,465,432,483,472,471,504,509,552,582,578,688,601,650,662,752,758,751,832,886,898,
959,992 ,1019,1100,1132,1167,1153,1170,1222,1294,1303,1307,1324,1356,1291,1352,1310,1332,1349,
1256,1258 ,1247,1182,1181,1116,1095,1050,1015,1014,1000,977,868,838,757,772,715,668,672,590,591
,597,509, 572,472,521,480,476,454,460,423,438,405,441,401,455,423,450,462,441,466,489,530,515,
505,587,557 ,585,572,586,608,608,686,690,749,695,741,739,798,792,773,830,805,792,808,821,841,
823,863,864, 869,870,863,915,924,905,862,902,896,893,889,835,869,889,915,912,913,860,799,827,
802,812,809,807 ,758,770,740,746,733,734,669,671,656,617,637,584,567,595,542,558,533,520,520,
502,477,480,449, 497,471,490,425,491,438,465,464,430,484,484,500,481,506,460,459,512,482,520,
522,494,549,582,584 ,585,654,622,610,634,654,674,671,704,722,736,722,747,806,812,772,783,792,
852,829,814,873,871, 835,838,790,810,771,798,756,763,808,738,735,700,663,676,659,628,625,597,
591,565,559,567,571,552 ,564,503,592,517,548,546,501,492,487,472,489,549,539,510,547,508,561,
497,506,507,507,507,524, 507,530,528,578,567,530,541,563,563,557,551,569,543,571,625,608,586,
627,664,625,684,656,725,775 ,737,779,763,825,851,837,885,926,877,969,964,1026,983,1014,1031,
1077,1142,1094,1093,1145,1125, 1093,1106,1131,1117,1116,1067,1102,1100,1029,953,976,923,924,897
,902,846,832,718,706,685,698, 660,641,659,576,584,557,521,560,498,491,506,498,440,467,432,436,
440,412,410,408,427,413,409,408 ,434,423,437,409,429,451,445,435,430,484,457,459,445,424,452,
445,473,486,466,472,503,513,449, 467,492,479,490,455,515,489,484,470,464,463,466,472,464,412,
414,447,418,434,416,385,397,374,374 ,368,388,353,383,381,353,354,362,328,363,327,363,326,368,
365,298,317,346,309,329,352,353,346, 330,328,329,331,349,327,336,322,330,333,305,346,326,306,
298,319,343,335,350,348,343,335,325,344 ,373,333,344,339,317,331,365,322,330,368,364,312,361,
357,350,322,347,352,335,367,330,334,367, 311,378,362,356,351,336,360,327,325,328,308,316,316,
319,340,341,334,285,338,306,337,350,336,303 ,316,324,365,312,310,340,323,335,323,312,344,363,
356,330,341,361,336,368,355,324,305,312,337, 358,375,343,341,331,349,341,340,354,374,342,339,
375,382,338,366,359,311,386,342,332,374,372,375 ,341,376,393,343,353,426,408,381,404,405,436,
446,456,441,454,486,459,518,537,531,505,536,561, 582,614,637,657,620,683,659,713,730,744,769,
750,790,704,751,763,755,765,789,782,748,757,712,739 ,687,666,684,665,632,619,609,632,582,605,
580,550,586,515,485,479,490,474,473,445,444,418,442, 379,407,414,387,385,361,377,405,347,351,
393,422,397,359,401,363,383,360,382,390,373,382,400,358 ,394,397,377,388,375,426,408,390,423,
411,429,441,438,438,444,466,460,433,428,450,472,460,457, 441,431,434,461,453,427,473,432,410,
417,487,424,476,450,427,448,405,436,431,448,419,403,439,436 ,485,431,430,463,424,464,395,483,
475,455,542,524,546,532,516,609,595,599,602,668,621,720,768, 731,761,776,754,862,856,850,959,
921,981,950,1007,1098,1059,1086,1152,1206,1135,1193,1169,1215, 1304,1297,1320,1432,1435,1441,
1444,1558,1544,1561,1666,1622,1687,1735,1706,1809,1922,1853,1957, 1980,1855,2026,2071,2063,2087
,2083,2160,2026,2001,2086,1998,2036,2043,1850,2014,1932,1977,1852, 1856,1830,1760,1718,1646,
1602,1545,1482,1490,1399,1328,1363,1265,1147,1177,1163,1132,1085,1033, 981,988,898,887,802,800,
811,776,799,733,741,759,660,667,678,660,617,631,633,594,584,569,623,578 ,568,539,599,603,600,
573,582,571,579,588,543,587,597,597,585,593,632,615,639,669,709,742,744, 815,831,906,927,1022,
1109,1154,1222,1233,1433,1491,1510,1589,1797,1865,2050,2157,2319,2481,2637 ,2890,2977,3190,3339
,3569,3610,3934,4048,4325,4415,4604,4699,4876,5154,5265,5369,5545,5493,5575 ,5714,5789,5928,
5949,5938,5901,5971,6014,5815,5825,5694,5445,5487,5355,5247,5055,5067,4806,4672 ,4395,4275,4221
,3947,3749,3543,3348,3222,3054,2945,2787,2604,2406,2245,2114,2044,1884,1749,1658 ,1565,1463,
1299,1304,1251,1141,1083,1092,1028,964,994,903,857,836,859,793,818,773,760,735,748, 731,708,700
,691,705,653,634,704,654,632,655,653,657,644,662,641,668,634,647,704,649,745,647,683 ,693,639,
653,658,674,699,680,703,693,703,736,748,789,823,791,800,855,872,898,1015,1041,1068, 1109,1218,
1220,1404,1510,1540,1738,1817,1982,2202,2325,2646,2878,3206,3485,3670,4058,4471,4918, 5435,5839
,6223,6807,7378,7976,8547,9078,9894,10645,11095,11836,12840,13688,14167,15154,15724, 16561,
17293,18288,18947,19378,19981,20523,21206,21811,22148,22725,23021,23501,23484,24094,24134, 24343
,23961,24013,23799,23665,23163,22917,22345,22123,21724,21032,20517,19743,18822,18350,17587,
16713,15958,15276,14155,13727,12844,12159,11319,10702,9829,9350,8668,7704,7460,6801,6141,5842,
5202,4768,4323,4061,3614,3327,3121,2885,2520,2337,2158,1886,1870,1730,1591,1432,1405,1301,1237,
 1199,1169,1071,1019,1033,958,981,964,884,862,846,923,834,824,894,875,840,851,877,859,920,887,
895,867,887,854,910,865,875,808,871,878,958,925,912,931,884,871,878,967,916,921,911,948,949,956
 ,984,982,996,1031,961,1041,1030,1013,1048,1020,1122,1103,1197,1122,1168,1166,1216,1234,1233,
1295,1321,1279,1321,1359,1422,1501,1541,1586,1627,1657,1704,1859,1727,1795,1911,2012,2047,2109,
 2182,2233,2372,2375,2429,2618,2632,2646,2819,2847,2967,2976,3065,3023,3187,3191,3252,3368,3350
, 3418,3437,3542,3461,3458,3511,3544,3605,3548,3443,3326,3437,3586,3380,3396,3297,3219,3206,
3163, 3092,3023,2976,2936,2734,2615,2818,2729,2598,2544,2460,2415,2396,2372,2250,2216,2178,2002
,2165, 2090,2082,2023,2056,1939,1974,2051,1931,1938,1982,1964,1897,1846,1883,1966,2008,1899,
1969,1926, 1908,1996,1953,2028,2009,2025,1915,2046,1998,2061,1990,2101,2036,2030,2029,2042,2027
,2130,2151, 2119,2166,2223,2121,2257,2279,2244,2273,2283,2327,2293,2312,2369,2358,2360,2392,
2417,2363,2406, 2412,2414,2546,2521,2464,2518,2594,2618,2549,2593,2476,2527,2649,2715,2669,2748
,2771,2857,2879, 2899,2890,2891,2918,2951,3018,3002,3051,3043,2934,2993,3157,3185,3129,3221,
3209,3315,3229,3319, 3464,3528,3518,3502,3581,3686,3719,3680,3906,3961,3879,4055,4047,4077,4175
,4332,4317,4543,4551, 4593,4900,5017,5080,5130,5134,5246,5417,5657,5901,5936,6033,6210,6405,
6483,6542,6749,6880,6936, 7268,7295,7427,7547,7646,7791,7877,7874,7904,7968,7904,8078,8153,8134
,8180,8297,8417,8148,8254, 8220,8162,8079,8301,8386,8126,7987,8058,7976,8113,7981,7881,7965,
7998,7926,7691,7673,7966,7705, 7818,7832,7991,7773,7780,7855,7921,8039,8144,8044,8151,8335,8503
,8342,8485,8642,8727,8968,9037, 8973,9286,9472,9467,9649,9633,9852,10087,10324,10455,10544,
10671,10723,10915,11142,11511,11370, 11767,11854,12030,12100,12551,12617,12970,13156,13173,13556
,14035,13927,14554,14687,14774,15226, 15195,15757,16083,16156,16280,16907,17065,17712,17816,
18071,18382,18764,19315,19362,19550,20389, 20653,20877,21672,21694,22271,22445,22773,23473,23780
,24216,24612,24919,25419,25889,26356,26655, 27013,27463,28239,28932,29076,29406,30525,30579,
31144,31481,31670,32470,32822,33354,33483,34402, 34691,35146,35908,36336,36851,37150,37975,38026
,38632,39310,39664,40183,40102,41029,41434,42113, 42382,42752,43332,43589,44660,45201,45332,
45652,46371,46950,47189,47419,48039,48300,48845,49391, 49563,50736,50760,50813,51345,51783,52317
,52077,53156,53270,53428,53676,54473,54911,55191,55081, 55411,56022,56171,56415,56042,57405,
57315,57685,58210,58000,58331,58283,58735,59244,59623,59415, 59791,59853,60559,60735,60174,60449
,60685,61229,61318,61072,61579,61947,61542,61872,62304,62042, 62301,62212,62331,62645,62827,
63027,62745,62643,63126,63198,63308,63000,63625,63539,63314,63434, 63613,63732,63337,63586,63961
,63401,63664,63382,63363,63167,62516,63287,63164,63811,63358,62960, 63058,63298,63002,62929,
62864,62814,62547,62532,62245,62734,62170,62748,61913,62155,62169,61630, 61773,61329,61714,61168
,61225,61584,61449,61443,61247,61445,61816,61913,61766,61879,62553,62069, 62767,62801,63584,
64331,65020,65601,65916,66887,67793,69130,69897,71488,72783,73867,75168,76931, 78633,79978,82379
,83725,86025,87889,90032,92146,94860,97142,99208,102240,103899,106554,109281, 111729,114053,
116401,119073,121053,123172,125016,127208,129671,131055,132664,134543,135633, 137326,137801,
138699,139156,139417,138971,139652,139539,138118,137578,136973,135182,133500, 131798,130274,
128197,125389,123221,120332,117842,113851,110543,107432,103640,99809,95733,92327, 88210,84098,
80526,76943,72796,68490,65378,61465,57688,54128,50967,47401,44181,41497,38624,35151, 33068,30305
,28066,25714,23793,21736,19949,18203,16443,15365,13955,12837,11643,10445,9662,8778, 8183,7438,
6737,6171,5828,5194,4740,4440,4057,3794,3737,3372,3131,2918,2779,2639,2519,2386,2240, 2142,2173
,2094,1989,1886,1801,1704,1635,1641,1624,1532,1478,1410,1384,1379,1345,1317,1213,1288, 1215,
1177,1164,1123,1108,1072,1001,1032,1021,973,933,874,881,886,796,813,772,799,802,744,770, 711,
679,689,685,628,659,635,583,613,577,617,563,525,571,553,526,501,487,470,502,476,462,464,449 ,
429,432,419,440,394,458,371,386,368,364,358,339,353,329,360,280,335,323,322,291,314,281,289,
269,324,286,264,265,309,280,266,235,268,269,251,250,238,233,274,257,226,256,229,235,245,227,248
 ,223,197,202,214,224,203,184,185,195,218,219,212,202,214,201,182,191,207,195,175,180,193,197,
169,194,179,189,182,216,179,181,190,176,131,195,188,187,174,181,160,180,159,163,173,152,194,173
 ,179,181,170,172,173,166,182,159,202,176,167,151,172,147,167,175,182,155,171,148,149,159,171,
163,161,138,150,159,159,141,171,150,156,169,130,148,144,154,148,125,150,148,159,149,155,149,152
 ,124,125,155,157,155,124,146,175,145,152,156,136,153,139,156,160,151,143,144,141,157,153,150,
145,164,141,149,155,151,126,142,163,163,159,147,153,158,154,172,160,161,166,175,156,157,155,158
 ,153,170,174,166,167,147,190,174,168,152,190,172,162,176,164,189,177,150,150,182,159,171,190,
156,134,161,191,152,163,163,145,144,132,119,140,169,152,146,142,138,128,134,130,131,147,104,139
 ,100,114,108,106,116,91,94,120,117,101,94,93,79,78,92,86,100,86,110,87,95,86,101,75,86,79,78,
88,75,91,91,94,97,84,80,82,95,96,112,102,92,91,97,106,98,101,99,116,90,118,104,128,130,126,95,
130,114,117,113,113,107,128,130,127,128,131,124,112,135,130,129,118,118,101,111,140,122,130,123
 ,111,115,117,118,102,108,126,99,132,102,96,107,103,91,100,115,96,78,98,121,109,107,95,81,125,
107,71,92,100,99,109,111,94,86,107,89,99,101,98,88,89,89,111,85,80,93,97,85,124,95,96,119,99,
87,96,113,110,89,107,103,116,92,103,104,114,104]
    y=np.array(channels)
    xl=len(y)
    x=np.arange(xl)
    fwhm_mult=2.5
    def cut(x0,hw):
        ix0=math.floor(x0+0.5)
        ihw=math.floor(hw+0.5)
        xmin=math.floor(ix0-ihw)
        if xmin<0:
            xmin=0
        xmax=math.floor(ix0+ihw)
        if xmax>=xl:
            xmax=xl-1
        return xmin,xmax

    def of(X, xw):
        x0,A, fwhm,b,k =X
        _=gauss(xw, x0, A, fwhm)+b+k*(xw-x0)
        return _
    def r_line(x0, A=None, fwhm=10, xtol=1e-8, width=None, plot=False):
        def fopt(X, xw, yw):
            _=of(X, xw)
            return sum((yw-_)**2)
        if width == None:
            width=fwhm
        hw=width/2.
        xmin,xmax=cut(x0, hw)
        if A == None:
            A=max(y[xmin:xmax])
            #print A
        X0=np.array([x0, A, fwhm, 0,0], dtype=float)
        xw=x[xmin:xmax]
        yw=y[xmin:xmax]
        Xopt=op.fmin(fopt, X0, args=(xw,yw), xtol=xtol, maxiter=10000, maxfun=10000)
        x0, A, fwhm, b, k =Xopt
        nxw=np.arange(xw[0], xw[-1], 0.25)
        fy=of(Xopt, nxw)
        if plot:
            p.fill_between(nxw,fy,(nxw-x0)*k+b, color=(0.7,0.3,0), alpha=0.5)
        return Xopt

    def ofp(X, xw):
        x0,A, fwhm, a0, a1 =X
        dxw=(xw-x0)
        _=gauss(xw, x0, A, fwhm)+a0+a1*dxw
        return _

    def r_line_zr(x0, A=None, fwhm=None, xtol=1e-8, width=None, plot=False):

        def fopt(X, x0, fwhm, xw, yw):
            A, a0, a1 = X
            X=[x0, A, fwhm, a0, a1]
            _=ofp(X, xw)
            return sum((yw-_)**2)

        if fwhm==None:
            raise ValueError, "fwhm should be defined"
        if width == None:
            width=fwhm
        hw=width/2.
        xmin,xmax=cut(x0, hw)
        if A == None:
            A=max(y[xmin:xmax])
            #print A
        X0=[A, 0,0]
        xw=x[xmin:xmax]
        yw=y[xmin:xmax]
        Xopt=op.fmin(fopt, X0, args=(x0, fwhm, xw,yw), xtol=xtol, maxiter=10000, maxfun=10000)
        A, a0, a1 =Xopt
        nxw=np.arange(xw[0], xw[-1], 0.25)
        Xopt=[x0, A, fwhm, a0, a1]
        fy=ofp(Xopt, nxw)
        if plot:
            dnxw=nxw-x0
            p.fill_between(nxw,fy,a0+a1*dnxw, color=(0.7,0.3,0), alpha=0.5)
        return Xopt


#    X0=np.array([80, np.max(y), 100, 0,0], dtype=float)
    e_fe= 6.4
    e_0 = 0.0086
    e_mo= 17.41
    e_zr= 15.774
    p.plot(x,y)
    x00, _, fwhm_0, b0, k0= r_line(80, width=len(x)/50, plot=True)
    print "FWHM0:", fwhm_0
    #fwhm_0=100
    w=15*fwhm_0/2.
    #x0_fe, _, fwhm_fe, b_fe, k_fe = recog(1370, fwhm=fwhm_0, width=w) # Fe
    x0_fe, _, fwhm_fe, b_fe, k_fe = r_line(1350, fwhm=fwhm_0, width=w, plot=True) # Fe
    s_k=(e_fe-e_0)/(x0_fe-x00)
    s_b=e_fe - (s_k*x0_fe)
    print "Scale:", s_k, s_b
    def to_chan(e):
        return (e-s_b)/s_k
    x0_mo=to_chan(e_mo)
    x0_zr=to_chan(e_zr)
    r_line(1000, fwhm=fwhm_0, width=w, plot=True)
    #recog(3255, fwhm=fwhm_0, width=w/2.)
    #recog(x0_mo, fwhm=fwhm_0, width=w, plot=True)
    _y=np.array([fwhm_0, fwhm_fe])

    def ffwhm(k, x):
        return _y-np.sqrt(x)*k

    k = op.leastsq(ffwhm, [1], args=np.array([e_0, e_fe]))

    fwhm_zr=k[0]*math.sqrt(e_zr)
    fwhm_mo=k[0]*math.sqrt(e_mo)

    #X=r_line(2920, fwhm=fwhm_0, width=w)
    #fwhm_X=math.sqrt((X[0]-b_fwhm)/k_fwhm)
    #r_line_fix(X[0], fwhm=fwhm_zr, width=w, plot=True)

    #r_line(1821, fwhm=fwhm_0, width=w, plot=True)
    print "fwhm:", fwhm_zr, k

    gain=1/s_k

    def Gc(E, E0, fwhm, fg):
        sigma = fwhm/fwhm_coef
        _1=sigma*fg
        _ = (sqrt_2pi*_1)
        _ = 1/_
        dE=E-E0
        _x= -((dE/_1)**2)/2.
        return _*np.exp(_x)

    def T(E, E0, fwhm, g, mult=1.):
        sigma = fwhm/fwhm_coef
        dE=E-E0
        _ef=math.exp(-1/(2*g**2))
        _0=g*sigma
        _1=2*_0*_ef
        _exp1=np.exp(mult*dE/_0)/_1
        _x=mult*dE/(sqrt_2*sigma)+1./(sqrt_2*g)
        return _exp1*fn.erfc(_x)

    def cou_approx(A, E, E0, fwhm, fg, fa, fb, ga, gb, A_mo, x0_mo):
        #print (E, E0, fwhm, fg, fa, fb, ga, gb)
        _ = Gc(E, E0, fwhm, fg)+fa*T(E, E0, fwhm, ga)+fb*T(E, E0, fwhm, gb, mult=-1)
        return A*_ + gauss(E, x0_mo, A_mo, fwhm)

    def cou_opt(X,  Ew, E0, fwhm, yw, A_mo, x0_mo):
        #print X
        A, fg, fa, fb, ga, gb = X
        return sum((cou_approx(A, Ew, E0, fwhm, fg, fa, fb, ga, gb, A_mo, x0_mo)-yw)**2)

    def cou_fmin(E, E0, fwhm, A_mo, x0_mo, X0=None, xtol=1e-3, xmin=0, xmax=None):
        if X0 == None:
            X0 = [1., 2.5, 1., 1., 8., 4.]
        if xmax == None:
            xmax=len(E)
        Ew=E[xmin:xmax]
        yw=y[xmin:xmax]
        return op.fmin(cou_opt, X0, args=(Ew, E0, fwhm, yw, A_mo, x0_mo), xtol=xtol, maxiter=10000, maxfun=10000)

    r_line_zr(x0_zr, fwhm=fwhm_zr, width=fwhm_zr*1.1, plot=True)
    _, A_mo, _,_,_ = r_line_zr(x0_mo, fwhm=fwhm_mo, width=fwhm_zr*1.1, plot=True)
    #p.show()
    #Coumpton Pike
    angle=90-2 #(degrees)
    rangle=angle*math.pi/180
    m0=510.996
    E0=e_mo
    Ec=E0 #seq(15.0,17.415, by=0.1)
    DE=(E0*Ec/m0)*(1-math.cos(rangle))
    print "DE:", DE

    x0_coumpton=to_chan(e_mo-DE)
    #p.plot(x, 6000000*Gc(x,x0_coumpton, fwhm=fwhm_mo, fg=2.))
    #p.plot(x, 3000000*T(x,x0_coumpton, fwhm=fwhm_mo, g=2))
    #p.plot(x, 3000000*T(x,x0_coumpton, fwhm=fwhm_mo, g=2, mult=-1))

    AA_mo=A_mo
    Xopt=[A, fg, fa, fb, ga, gb]=cou_fmin(x, x0_coumpton,
        fwhm_mo, AA_mo,x0_mo, xmin=3155, xmax=3700)
    p.plot(x, cou_approx(A, x, x0_coumpton, fwhm_mo,
        fg, fa, fb, ga, gb, AA_mo,x0_mo)) # Need a common amplitude
    print Xopt
    p.show()


if __name__=='__main__':
    test1()
