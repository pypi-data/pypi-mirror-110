In the travel demand model, the performance of traffic systems is evaluated via traffic assignment for assessing the impacts of transportation improvement projects. The fundamentally important volume-delay functions (VDFs) have been used as the building blocks to account for the effects of traffic flow on roadway segments’ capacities. 

The data2supply is a data-driven calibration package for traffic flow model calibration, Bureau of Public Roads (BPR) function calibration, and the queueing characterization for transportation planners, engineers, and researchers.



The development of data2supply  is motivated by the following perspectives.

**1. Support the implementation of traffic assignment model **

The development of the package is motivated by the evaluation of the current traffic assignment model  and implement a refined or modified BPR function. 

To facilitate the development of the package, the users should provide the certain timestamp (e.g., 15-minutes)speed-flow matched data using link_performance.csv

the calibration will be conducted under different area types (AT) and facility types (FT). 

**2. Data-driven calibration and validation tool for integrated traffic analysis** 

The development goal of data2supply aims to provide an integrated open-source package for data processing workflow, parameter estimation in the traffic stream model (i.e. ultimate capacity, critical density, free-flow speed, and the speed at capacity as well as the validation of the traffic assignment results. Three calibration methods, namely, volume-based method (VBM), density-based method (DBM), (proposed) queue-based method (QBM), are embedded in the package to estimate alpha/beta” in the BPR function

Combined with the traffic assignment/simulation engine TRANSCAD, the data2supply package aims to:

- provide an open-source code to enable planners and engineers to expand their capabilities of mining the underlying information from traffic data.

- provide a data-driven process that allows estimating period-based demand flows for oversaturated traffic conditions. 

- present the calibration results to other users by visualizing traffic flow fundamental and volume delay relationship diagram.

- provide a convenient tool for validating static traffic assignment results from TRANSCAD in transportation planning and optimization processes.

**3. Adopting open network standard of GMNS**

The General Modeling Network Specification (GMNS) defines a common human and machine-readable format for sharing routable road network files. It is designed to be used in multi-modal static and dynamic transportation planning and operations models. data2supply applies the general travel network format specification to advance the field through flexible and efficient support, education, guidance, encouragement, and incubation. Further details can be found in https://zephyrtransport.org/projects/2-network-standard-and-tools/

Check out the standard GMNS data sets at

https://github.com/zephyr-data-specs/GMNS/tree/master/Small_Network_Examples/Lima/GMNS

https://github.com/xzhou99/NeXTA-GMNS/tree/master/examples/GMNS_Small_Network_Examples/Lima/GMNS

One can build your own GMNS data set.

A simple 6-node example with agent files can be found at https://github.com/xzhou99/NeXTA-GMNS/tree/master/examples/GMNS_AMS_Networks/6-node_network

 

**4. New VDF calibration method**

This package also attempts to provide a theoretically consistent and practically effective framework for a data-driven VDF calibration process. By defining the queueing demand in the D/C ratio in the BPR function, the proposed Queue-based method (QBM) provides a new method for the BPR calibration and bridges the gap between the different temporal resolution of the demand-supply relation. The new QBM is a peak-period demand-oriented calibration framework that closely connects traffic flow measures and queue dynamics (e.g., bottleneck, evolutions, and capacity drop), which has some characteristics different from other methods. 



Input files: 

**Link performance file following GMNS format** 

The observed data (link counts and speed files) are systematically organized using link performance files. The link performance file contains each link’s time-dependent information, such as speed, volume, and some notes. The detailed field names of link_performance.csv are listed in the following. 



| **Field Name**    | **Description**                                              | **Sample Value** |
| ----------------- | ------------------------------------------------------------ | ---------------- |
| link_id           | Link identification number of a road segment                 | 10024AB          |
| lanes             | Number of lanes of a link                                    | 2                |
| length            | Length of the link (units: miles or km)                      | 0.22148          |
| from_node_id      | Upstream node of the link                                    | 12391            |
| to_node_id        | Downstream node of the link                                  | 27808            |
| FT                | Facility type                                                | 6                |
| AT                | Area type                                                    | 1                |
| time_period       | Timestamp of an observation                                  | 000_0015         |
| assignment_period | Static traffic assignment period (peak periods, e.g. a.m.  or p.m.) | 0600_0900        |
| volume            | Observed link count                                          | 50               |
| speed             | Observed link speed                                          | 24               |
| speed_limit       | Speed limit of the link                                      | 35               |
| date              | Date of the data                                             | 1/1/2018         |

 **Example:** 

![image-20210511011448546](C:\Users\xinwu\AppData\Roaming\Typora\typora-user-images\image-20210511011448546.png)



**Remark 1:** The pair of FT and AT means a VDF (volume delay function) type. For example, we can follow the VDF codes as follows. However, the users can also define their own VDF types 

| Area Type        |               |                  |                |                      |                          |                      |                      |                    |                |                       |                    |                    |                  |                 |      |      |
| ---------------- | ------------- | ---------------- | -------------- | -------------------- | ------------------------ | -------------------- | -------------------- | ------------------ | -------------- | --------------------- | ------------------ | ------------------ | ---------------- | --------------- | ---- | ---- |
| HOV  Lane (0)    | Freeways  (1) | Expressways  (2) | Collectors (3) | 6  Leg Arterials (4) | Centroid  Connectors (5) | Major  Arterials (6) | Unmetered  Ramps (7) | Metered  Ramps (8) | C/D  Roads (9) | Arizona  Parkway (10) | Unpaved  Road (11) | Transit  Only (12) | Light  Rail (13) | Walk  Only (14) |      |      |
| (1) CBD          | 100           | 101              | 102            | 103                  | 104                      | 105                  | 106                  | 107                | 108            | 109                   | 110                | 111                | 112              | 113             | 114  |      |
| (2) Outlying CBD | 200           | 201              | 202            | 203                  | 204                      | 205                  | 206                  | 207                | 208            | 209                   | 210                | 211                | 212              | 213             | 214  |      |
| (3) Mixed Ur­ban | 300           | 301              | 302            | 303                  | 304                      | 305                  | 306                  | 307                | 308            | 309                   | 310                | 311                | 312              | 313             | 314  |      |
| (4) Suburban     | 400           | 401              | 402            | 403                  | 404                      | 405                  | 406                  | 407                | 408            | 409                   | 410                | 411                | 412              | 413             | 414  |      |
| (5) Rural        | 500           | 501              | 502            | 503                  | 504                      | 505                  | 506                  | 507                | 508            | 509                   | 510                | 511                | 512              | 513             | 514  |      |



**Remark 2:** The time period and assignment period follow the **HHMM time format** (e.g., using HHMM_HHMM to express a time interval). For example, the timestamp of the link performance might be 15 minutes(e.g., 0600_0615). In travel demand models, peak periods are defined as time windows where travel demands (OD matrices) are pre-specified and STA will be performed in the following: 

a.   AM (6:00am-9:00am, 0600_0900)     

b.   MD (9:00am-2:00pm, 0900_1400) 

c.   PM (2:00pm-6:00pm, 1400_1800)

d.   NT (18:00pm-6:00am, 1800_0600)



**Simple examples:** 

calibrate traffic flow models 

```python
import data2supply as ds
# calibrate traffic flow models (when facility type = 1 and area type =1 )
ds.calibrateFundamentalDiagram(ft_list=[1], at_list=[1])
# calibrate traffic flow models (for each combination of facility types and area types )
ds.calibrateFundamentalDiagram()
```



```Python
import data2supply as ds

# calibrate VDF (or BPR) functions (when facility type = 1 and area type =1 )
ds.calibrateVdfCurve(ft_list=[1], at_list=[1])

# calibrate VDF (or BPR) functions (for each combination of facility types and area types )
ds.calibrateVdfCurve()
```

