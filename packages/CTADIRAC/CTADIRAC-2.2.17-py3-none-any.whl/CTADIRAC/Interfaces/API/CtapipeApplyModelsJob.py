"""
  Simple Wrapper on the Job class to run ctapipe-apply-models
"""

__RCSID__ = "$Id$"

# generic imports
import json
from copy import deepcopy

# DIRAC imports
from CTADIRAC.Interfaces.API.ProcessingJob import ProcessingJob


class CtapipeApplyModelsJob(ProcessingJob):
    """Job extension class for ctapipe apply models"""

    def __init__(self, **kwargs):
        """Constructor"""
        super().__init__(**kwargs)
        # defaults
        self.setName("ctapipe_apply-models")
        self.setType("ApplyModel")
        self.prog_name = "ctapipe-apply-models"
        self.options = ""
        self.data_level = 2

    def set_output_metadata(self, metadata):
        """Set meta data

        Parameters:
        metadata -- metadata dictionary from input configuration
        """
        # # Set directory meta data
        self.output_metadata["array_layout"] = metadata["array_layout"]
        self.output_metadata["site"] = metadata["site"]
        self.output_metadata["particle"] = metadata["particle"]

        try:
            phiP = metadata["phiP"]["="]
        except BaseException:
            phiP = metadata["phiP"]
        self.output_metadata["phiP"] = phiP
        try:
            thetaP = metadata["thetaP"]["="]
        except BaseException:
            thetaP = metadata["thetaP"]
        self.output_metadata["thetaP"] = thetaP
        if metadata.get("sct"):
            self.output_metadata["sct"] = metadata["sct"]
        else:
            self.output_metadata["sct"] = "False"
        self.output_metadata[self.program_category + "_prog"] = self.prog_name
        self.output_metadata[self.program_category + "_prog_version"] = self.version
        self.output_metadata["data_level"] = self.data_level
        self.output_metadata["configuration_id"] = self.configuration_id
        self.output_metadata["MCCampaign"] = self.MCCampaign

    def set_executable_sequence(self, debug=False):
        """Setup job workflow by defining the sequence of all executables
        All parameters shall have been defined before that method is called.
        """
        i_step = 0
        # step 1 -- debug
        if debug:
            ls_step = self.setExecutable("/bin/ls -alhtr", logFile="LS_Init_Log.txt")
            ls_step["Value"]["name"] = "Step%i_LS_Init" % i_step
            ls_step["Value"]["descr_short"] = "list files in working directory"
            i_step += 1

        # step 2
        sw_step = self.setExecutable(
            "cta-prod-setup-software",
            arguments="-p %s -v %s -a stage1 -g %s"
            % (self.package, self.version, self.compiler),
            logFile="SetupSoftware_Log.txt",
        )
        sw_step["Value"]["name"] = "Step%i_SetupSoftware" % i_step
        sw_step["Value"]["descr_short"] = "Setup software"
        i_step += 1

        # step 3 : download model by query
        model_metadata = deepcopy(self.output_metadata)
        model_metadata.pop("particle")
        if "energy_model.pkl" in self.options:
            model_metadata["analysis_prog"] = "ctapipe-train-energy-regressor"
            argument_list = []
            for key, value in model_metadata.items():
                argument_list.append(key + "=" + str(value))

            get_step0 = self.setExecutable(
                "cta-prod-get-file-by-query",
                arguments=f"{' '.join(argument_list)}",
                logFile="DownloadEnergyModel_Log.txt",
            )
            get_step0["Value"]["name"] = "Step%i_DownloadEnergyModel" % i_step
            get_step0["Value"]["descr_short"] = "Download Energy Model"
            i_step += 1

        if "classifier_model.pkl" in self.options:
            model_metadata["analysis_prog"] = "ctapipe-train-particle-classifier"
            argument_list = []
            for key, value in model_metadata.items():
                argument_list.append(key + "=" + str(value))

            get_step1 = self.setExecutable(
                "cta-prod-get-file-by-query",
                arguments=f"{' '.join(argument_list)}",
                logFile="DownloadClassifierModel_Log.txt",
            )
            get_step1["Value"]["name"] = "Step%i_DownloadClassifierModel" % i_step
            get_step1["Value"]["descr_short"] = "Download Classifier Model"
            i_step += 1

        # step 4 run apply models
        proc_step = self.setExecutable(
            "./dirac_ctapipe-apply-models_wrapper",
            arguments=f"{self.options}",
            logFile="ctapipe_apply_models_Log.txt",
        )
        proc_step["Value"]["name"] = "Step%i_ctapipe_apply_models" % i_step
        proc_step["Value"]["descr_short"] = "Run ctapipe apply models"
        i_step += 1

        # step 5 set meta data and register Data
        meta_data_json = json.dumps(self.output_metadata)
        file_meta_data_json = json.dumps(self.output_file_metadata)

        # register Data
        data_output_pattern = "./Data/*.h5"
        dm_step = self.setExecutable(
            "cta-prod-managedata",
            arguments="'%s' '%s' %s '%s' %s %s '%s' Data"
            % (
                meta_data_json,
                file_meta_data_json,
                self.base_path,
                data_output_pattern,
                self.package,
                self.program_category,
                self.catalogs,
            ),
            logFile="DataManagement_Log.txt",
        )
        dm_step["Value"]["name"] = f"Step{i_step}_DataManagement"
        dm_step["Value"][
            "descr_short"
        ] = "Save data files to SE and register them in DFC"
        i_step += 1

        # step 6 failover step
        failover_step = self.setExecutable(
            "/bin/ls -l", modulesList=["Script", "FailoverRequest"]
        )
        failover_step["Value"]["name"] = f"Step{i_step}_Failover"
        failover_step["Value"]["descr_short"] = "Tag files as unused if job failed"
        i_step += 1

        # Step 7 - debug only
        if debug:
            ls_step = self.setExecutable("/bin/ls -Ralhtr", logFile="LS_End_Log.txt")
            ls_step["Value"]["name"] = f"Step{i_step}_LSHOME_End"
            ls_step["Value"]["descr_short"] = "list files in Home directory"
            i_step += 1
