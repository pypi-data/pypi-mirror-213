import sys
sys.path.append("..") # Adds higher directory to python modules path.
import numpy as np
import matplotlib.pyplot as plt
from typing import Union

from ..properties import  *



"""
TODO:
Create  abstract class for properties like tensile strength, tensile modulus, etc, with pass, so using diffrent norms and materials will be easier
Move calculation of real values into method of engineering values
Add decorators

SOURCES:

https://professorkazarinoff.github.io/Engineering-Materials-Programming/07-Mechanical-Properties/mechanical-properties-from-stress-strain-curves.html


"""


class sample:
    """Initialization of sample class

    That's class for each of your tested sample

    Parameters
        ----------
        name : str
        name of your sample etc. Neat PLA
        thickness : float
        thickness of your sample
        width : float
        width of your sample
        elongation_array : Union[list, np.array]
        elongation array from your tensile machine
        force_array : Union[list, np.array]
        forces obtained from your tensile machine
        stress_array : Union[list, np.array]
        calculated stresses
        strain_array : Union[list, np.array]
        calculated strains
        manufactured_method : str
        how your sample was made, etc. by FDM or injection method, just for description
        comments : str
        any comments describing your sample
        force_units : str
        force units of your force array
        lenght_units : str
        length units of your force array

    Raises
        ------
        ValueError
        Raises ValueError while stress/strains or width/thickness are not defined
    
    Examples
        --------
        elongation_array=df["elongation"]
        force_array=df["force"]

        # This uses N ewtons and mm by default to ensure [N/mm^2] as it is equal to MPa
        example=mt.sample(name="your sample name",
        thickness = 5,
        width= 5,
        elongation_array=elongation_array,
        force_array=force_array
        )
        """

    def __init__(self,name: str,
                     thickness:float = None,
                     width:float = None,
                     elongation_array: Union[list, np.array] =None,
                     force_array: Union[list, np.array] =None,
                     stress_array: Union[list, np.array] =None,
                     strain_array: Union[list, np.array] =None,
                     manufactured_method: str=None,
                     comments: str=None,
                     force_units: str="N",
                     lenght_units: str="mm"):
            
        


            self.name=name
            self.thickness, self.width= thickness,width
            self.eng_values=engineering_values(name=name,
                                               force_units=force_units,
                                               lenght_units=lenght_units,
                                               thickness=thickness,
                                               width=width
                                               )
            self.force_units, self.lenght_units=force_units,lenght_units
            if stress_array is None and strain_array is None:
                if elongation_array is None and force_array is None:
                    raise ValueError("None of elongation/force or stress/strain arrays are defined!")
                elif thickness is None:
                    raise ValueError("Thickness is not defined!")
                elif width is None:
                    raise ValueError(" Width is not defined!")
                else:
                    self.elongation_array=elongation_array
                    self.force_array=force_array
                    self.eng_values.calculate(thickness=self.thickness,
                                              width=self.width,
                                              elongation_array=elongation_array,
                                              force_array=force_array)

            else:
                self.eng_values.set(stress_array, strain_array)

    def calculate_real_values(self):
        self.real_values=real_values_class(name=self.name,
                                           thickness=self.thickness,
                                           width=self.width,
                                           force_units=self.force_units,
                                           lenght_units=self.lenght_units
                                           )
        self.real_values.calculate(self.eng_values.stress,
                                   self.eng_values.strain)            
    def plot(self, show=False):
        """Method for plotting the results

            This method can be used to plot your engineering stress-strain curve. If you wanna show it instantly use
            parameter show as True

            Parameters
            ----------
            show : bool
                It it equal to matplotlib.pyplot function show

            Examples
            --------
            FIXME: Add docs.

            """
        plt.plot(self.elongation_array,self.force_array, label=self.name)
        plt.title(self.name)
        plt.ylabel(f"Force [{self.force_units}]")
        plt.xlabel(f"Strain [{self.lenght_units}]")
        plt.legend()
        if show:
                plt.show()        


                
        
    def composition_from_name(delimiter: str, percent_sign="p"):
        """
        TODODO baby shark
        method to obtain material ingridiens from name, as I usually name files extracted from machine with code allowing me to get that information from filename
        Finds the proportional range of a stress-strain curve by searching for a derivative.
        
    Parameters:
        strain (array-like): An array of strain values.
        stress (array-like): An array of corresponding stress values.
        n: An count of chunks to divide stress/strain array
        
    Returns:n
            Sets start and end of proportional range points
        """
        pass
    
class engineering_values:
        def __init__(self,
                     thickness,
                     width,
                     name=None,
                     force_units="N",
                     lenght_units="mm"
                     ):
            """initializer of engineering values class

            This class is used to menage the properties of engineering values

            Parameters
            ----------
            name : str
                name for your sample

            Examples
            --------
            FIXME: Add docs.

            """
            
            self.name=name
            self.force_units = force_units
            self.lenght_units=lenght_units
            self.thickness=thickness,
            self.width=width
            self.stress, self.strain=None,None
        def calculate(self,
                      thickness:float,
                      width:float,
                      elongation_array,
                      force_array,
                      ):
            """Calculates the engineering stress and strain

            This method is used to calculate engineering stress and strain from height

            Parameters
            ----------
            thickness : float
                smaller initial dimension of the rectangular cross-section in the central part of test specimen
            width : float
                larger initial dimension of the rectangular cross-section in the central part of the test specimen
            elongation_array : list
                list of the sample elongation
            force_array : list
                list of the forces from the machinge
            force_units : str
                Units used as force units. Newtons [N] by default. Use shorten strings, as it is used in output
            lenght_units : str
                Units used for lenght, mm by default. Use short strings, as they are used in output. If you wanna use percent, just use % sign or percent
            """
            

            if self.lenght_units=="%" or self.lenght_units=="percent":
                self.percent_strain=True
            else:
                self.percent_strain=False


            if  self.stress is  None and self.strain is None:
                initial_area=thickness*width
                self.stress=[force/initial_area for force in force_array]
                if self.percent_strain:
                    self.strain=[strain for strain in elongation_array]
                else:
                    self.strain=[strain*0.01 for strain in elongation_array]

            self.strength=self.calculate_strength(self.stress,
                                                  self.strain)
            
            self.at_break=self.calculate_at_break(self.strain,
                                                  self.stress)
            
            self.yield_strength=self.calculate_yield_strength(self.stress,
                                                              self.strain)
            self.tensile_modulus=self.calculate_tensile_modulus()

        class calculate_strength:
            def __init__(self,strain: np.array,stress:np.array):
                """Strenght is according to ISO-527-1 first maximum local value

                Parameters
                ----------
                strain : np.array
                    strain array
                stress : np.array
                    stress array

                Examples
                --------
                FIXME: Add docs.

                """
                
                strength = properties.strenght(strain,stress)
                self.value=strength.value
                self.strain=strength.strain

        class calculate_yield_strength:
            def __init__(self, stress: np.array, strain: np.array):
                """
                Yield strenght  is according to ISO-527-1 strain increase without stress increase. 

                Parameters
                ----------
                stress : np.array
                    stress numpy array
                strain : np.array
                    strain numpy array

                Examples
                --------
                FIXME: Add docs.

                """
                yield_strenght=properties.yield_strenght(stress, strain)
                self.value, self.strain=yield_strenght.value,yield_strenght.strain
        class calculate_at_break:
            """
            This class calculates values at the brain according to ISO 527-1
            """
            def __init__(self,stress, strain):
                at_break=properties.at_break(stress, strain)
                self.stress=at_break.stress
                self.strain=at_break.strain


        def calculate_tensile_modulus(self,
                                      plot=False,
                                      r2=True,
                                      output=True,
                                      lower_limit=0.05,
                                      upper_limit=0.25
                                      ):
            """            Tensile, or Young's modulus is the slope of strain/stress curve, between strains equals to 0.05 and 0.25 percent according to DIN ISO 527-1

            Parameters
            ----------
            plot : bool
                Put True for use pyplot on the tensile modulus part
            r2 : Put coeffitient 	of determination into pyplot label
                Put coeffitient of determination into pyplot label
            output : bool
                Print the output of this method
            lower_limit : float
                lower limit of the measurement boundary
            upper_limit : float
                upper limit of the measurement boundary

            Examples
            --------
            FIXME: Add docs.

            """

            E=properties.tensile_modulus(self.stress,
                                         self.strain,
                                         percent_strain=self.percent_strain
                                         )
            if plot:
                label=rf"Young's modulus {int(E.tensile_modulus)} $\left[\frac{{{self.force_units}}}{{{self.lenght_units}^2}}\right]$"
                if r2:
                    label+="\n"+rf"$R^{{{2}}}={E.r2}$"
                    plt.plot(E.module_strain,
                             E.module_stress,
                             label=label
                             )
            if output:
                print(f"Tensile modulus is equal to {int(E.tensile_modulus)} [{self.force_units}/{self.lenght_units}^2]")
                return   E.tensile_modulus

                
        def set(self,
                engineering_stress: Union[list, np.array] =None,
                engineering_strain:Union[list, np.array] =None,
                # TODO: gives TypeError: only size-1 arrays can be converted to Python scalars while using numpy array
                # TODO: gives KeyKerrr None
                # TODO: in general this method does not work yet!
                ):
            """Method to set engineering stress and engineering strain

            Parameters
            ----------
            engineering_stress : list
                array of engineering stress
            engineering_strain : list
                array of engineering strain

            Examples
            --------
            FIXME: Add docs.

            """
            
            self.stress, self.strain=engineering_stress, engineering_strain
            self.calculate(thickness=self.thickness,
                           width=self.width,
                           elongation_array=None,
                           force_array=None)
            

        def plot(self, show=False):
            """Method for plotting the results

            This method can be used to plot your engineering stress-strain curve. If you wanna show it instantly use
            parameter show as True

            Parameters
            ----------
            show : bool
                It it equal to matplotlib.pyplot function show

            Examples
            --------
            FIXME: Add docs.

            """
            plt.plot(self.strain,self.stress, label=self.name)
            plt.title(self.name)
            plt.ylabel(rf"Stress $\left[\frac{{{self.force_units}}}{{{self.lenght_units}^2}}\right]$")
            plt.xlabel(f"Strain [{self.lenght_units}]")
            plt.legend()
            if show:
                plt.show()

class real_values_class(engineering_values):

        def __init__(self, name,
                     thickness,
                     width,
                     force_units,
                     lenght_units,
                     ):
            self.force_units=force_units
            self.lenght_units=lenght_units
            if lenght_units=="%" or lenght_units=="percent":
                self.percent_strain=True
            else:
                self.percent_strain=False

    
            engineering_values.__init__(self,
                                        name=name,
                                        thickness=thickness,
                                        width=width
                                        )
            self.name=name + " [real]"
            width=self.width
            super().__init__(self,
                             width=width,
                             name=self.name
                             )

        def calculate(self, stress, strain):
            """
                Calculates the true stress and strain, from engineering values.
                Read more there:
                        https://courses.ansys.com/index.php/courses/topics-in-metal-plasticity/lessons/how-to-define-a-multilinear-hardening-plasticity-model-lesson-1/
            
                Parameters:
                        strain (array-like): An array of strain values.
                        stress (array-like): An array of corresponding stress values.
                        n: An count of chunks to divide stress/strain array
            
                Returns:
                    A tuple (start_strain, end_strain) representing the proportional range of the stress-strain curve.
            """
            self.stress=[stress_val*(1+strain_val) for stress_val, strain_val in zip(stress, strain)]
            self.strain=[np.log(1+strain_val) for strain_val in strain]

            self.strength=self.calculate_strength(self.stress,
                                                  self.strain)
            
            self.at_break=self.calculate_at_break(self.strain,
                                                  self.stress)
            
            self.yield_strength=self.calculate_yield_strength(self.stress,
                                                              self.strain)
            self.tensile_modulus=self.calculate_tensile_modulus()            



        # def plot(self, show: bool=False):
        #     plt.plot(self.strain,self.stress, label=self.name)
        #     plt.title("real")
            
        #     plt.legend()
        #     if show:
        #         plt.show()

