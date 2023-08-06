from ERLANG.settings import output
from ERLANG.settings import request

# =============================================================================
# ERLANG BLENDING FUNCTIONS
# In the blending model, agents will work on inbound as well as outbound calls. 
# If an agent becomes available, they will prioritize inbound calls and will 
# only take on outbound calls when other agents are left idle.
# =============================================================================
    
class SLA():
    """
    Parameters
    ----------
    Forecast : float
        The average number of arrivals per unit of time. (Forecast ≥ 0)
    AHT : float
        The Average Handling Time of a call. (AHT > 0)
    Agents : float
        Represents the number of agents; it can be real. (Agents ≥ 0)
    Awt : float
        The Acceptable Waiting Time is the maximum allowed waiting time.
        Customers that wait shorter than the Awt have received, per definition,
        a good service. The service level is defined as the percentage of 
        customers that are served within the Awt. The time unit is the same as 
        the others and, hence, is not necessarily in seconds! (Awt ≥ 0)
    Threshold : float
        The number of agents that are kept idle before taking outbound calls into 
        service. (Threshold ≤ Agents)
        
    Returns
    -------
    float
        The expected service level.
    """
   
    def __new__(cls,Forecast:float,AHT:float,Agents:float,Awt:float,Threshold:float):
        output['function']='serviceLevelBlending'
        for i in SLA.__new__.__annotations__:
            output[i]=locals()[i]
        return request(output)

class ASA():
    
    def __init__(self):
         return None
     
    """
    Parameters
    ----------
    Forecast : float
        The average number of arrivals per unit of time. (Forecast ≥ 0)
    AHT : float
        The Average Handling Time of a call. (AHT > 0)
    Agents : float
        Represents the number of agents; it can be real. (Agents ≥ 0)
    Threshold : float
        The number of agents that are kept idle before taking outbound calls into 
        service. (Threshold ≤ Agents)
    
    Returns
    -------
    float
        The average speed of answer.
    """
   
    def __new__(cls,Forecast:float,AHT:float,Agents:float,Threshold:float):
        output['function']='waitingtimeThresholdBlending'
        for i in ASA.__new__.__annotations__:
            output[i]=locals()[i]
        return request(output)
    
    class SLA():
        """
        Parameters
        ----------
        Forecast : float
            The average number of arrivals per unit of time. (Forecast ≥ 0)
        AHT : float
            The Average Handling Time of a call. (AHT > 0)
        Agents : float
            Represents the number of agents; it can be real. (Agents ≥ 0)
        SL : float
            The expected Service Level of an arbitrary non-blocked customer. (0 < SL < 1)
        Awt : float
            The Acceptable Waiting Time is the maximum allowed waiting time.
            Customers that wait shorter than the Awt have received, per definition,
            a good service. The service level is defined as the percentage of 
            customers that are served within the Awt. The time unit is the same as 
            the others and, hence, is not necessarily in seconds! (Awt ≥ 0)
            
        Returns
        -------
        float
            The average speed of answer based on the service-level objective.
        """
        
        def __new__(cls,Forecast:float,AHT:float,Agents:float,SL:float,Awt:float):
            output['function']='waitingtimeServiceLevelBlending'
            for i in ASA.SLA.__new__.__annotations__:
                output[i]=locals()[i]
            return request(output)


class OCCUPANCY():
    """
    Parameters
    ----------
    Forecast : float
        The average number of arrivals per unit of time. (Forecast ≥ 0)
    AHT : float
        The Average Handling Time of a call. (AHT > 0)
    Agents : float
        Represents the number of agents; it can be real. (Agents ≥ 0)
    Threshold : float
        The number of agents that are kept idle before taking outbound calls into 
        service. (Threshold ≤ Agents)
    
    Returns
    -------
    float
        The occupancy of the agents.
    """

    def __new__(cls,Forecast:float,AHT:float,Agents:float,Threshold:float):
        output['function']='occupancyThresholdBlending'
        for i in OCCUPANCY.__new__.__annotations__:
            output[i]=locals()[i]
        return request(output)
    
    class SLA():
        """
        Parameters
        ----------
        Forecast : float
            The average number of arrivals per unit of time. (Forecast ≥ 0)
        AHT : float
            The Average Handling Time of a call. (AHT > 0)
        Agents : float
            Represents the number of agents; it can be real. (Agents ≥ 0)
        SL : float
            The expected Service Level of an arbitrary non-blocked customer. (0 < SL < 1)
        Awt : float
            The Acceptable Waiting Time is the maximum allowed waiting time.
            Customers that wait shorter than the Awt have received, per definition,
            a good service. The service level is defined as the percentage of 
            customers that are served within the Awt. The time unit is the same as 
            the others and, hence, is not necessarily in seconds! (Awt ≥ 0)
            
        Returns
        -------
        float
            The occupancy of the agents based on the service-level objective.
        """
       
        def __new__(cls,Forecast:float,AHT:float,Agents:float,SL:float,Awt:float):
            output['function']='occupancyServiceLevelBlending'
            for i in OCCUPANCY.SLA.__new__.__annotations__:
                output[i]=locals()[i]
            return request(output)
    
class OUTBOUND():
    """
    Parameters
    ----------
    Forecast : float
        The average number of arrivals per unit of time. (Forecast ≥ 0)
    AHT : float
        The Average Handling Time of a call. (AHT > 0)
    Agents : float
        Represents the number of agents; it can be real. (Agents ≥ 0)
    Threshold : float
        The number of agents that are kept idle before taking outbound calls into 
        service. (Threshold ≤ Agents)
    
    Returns
    -------
    float
        The average number of outbound calls per unit of time.
    """
    
    def __new__(cls,Forecast:float,AHT:float,Agents:float,Threshold:float):
        output['function']='outboundThresholdBlending'
        for i in OUTBOUND.__new__.__annotations__:
            output[i]=locals()[i]
        return request(output)
    
    class SLA():
        """
        Parameters
        ----------
        Forecast : float
            The average number of arrivals per unit of time. (Forecast ≥ 0)
        AHT : float
            The Average Handling Time of a call. (AHT > 0)
        Agents : float
            Represents the number of agents; it can be real. (Agents ≥ 0)
        SL : float
            The expected Service Level of an arbitrary non-blocked customer. (0 < SL < 1)
        Awt : float
            The Acceptable Waiting Time is the maximum allowed waiting time.
            Customers that wait shorter than the Awt have received, per definition,
            a good service. The service level is defined as the percentage of 
            customers that are served within the Awt. The time unit is the same as 
            the others and, hence, is not necessarily in seconds! (Awt ≥ 0)
            
        Returns
        -------
        float
            The average number of outbound calls per unit of time based on the 
            service-level objective.
        """
       
        def __new__(cls,Forecast:float,AHT:float,Agents:float,SL:float,Awt:float):
            output['function']='outboundServiceLevelBlending'
            for i in OUTBOUND.SLA.__new__.__annotations__:
                output[i]=locals()[i]
            return request(output)
        
class THRESHOLD():
    """
    Parameters
    ----------
    Forecast : float
        The average number of arrivals per unit of time. (Forecast ≥ 0)
    AHT : float
        The Average Handling Time of a call. (AHT > 0)
    Agents : float
        Represents the number of agents; it can be real. (Agents ≥ 0)
    SL : float
        The expected Service Level of an arbitrary non-blocked customer. (0 < SL < 1)
    Awt : float
        The Acceptable Waiting Time is the maximum allowed waiting time.
        Customers that wait shorter than the Awt have received, per definition,
        a good service. The service level is defined as the percentage of 
        customers that are served within the Awt. The time unit is the same as 
        the others and, hence, is not necessarily in seconds! (Awt ≥ 0)
    
    Returns
    -------
    float
        The threshold such that the service-level objective is satisfied.
    """
    
    def __new__(cls,Forecast:float,AHT:float,Agents:float,SL:float,Awt:float):
        output['function']='thresholdBlending'
        for i in THRESHOLD.__new__.__annotations__:
            output[i]=locals()[i]
        return request(output)
    
