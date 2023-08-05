"""Resources that represent collections of predictors."""
from uuid import UUID
from typing import TypeVar, Optional, Union

from citrine._session import Session
from citrine._utils.functions import migrate_deprecated_argument
from citrine.resources.module import AbstractModuleCollection
from citrine.informatics.data_sources import DataSource
from citrine.informatics.predictors import Predictor, GraphPredictor

CreationType = TypeVar('CreationType', bound=Predictor)


class PredictorCollection(AbstractModuleCollection[Predictor]):
    """Represents the collection of all predictors for a project.

    Parameters
    ----------
    project_id: UUID
        the UUID of the project

    """

    _path_template = '/projects/{project_id}/modules'
    _individual_key = None
    _resource = Predictor
    _module_type = 'PREDICTOR'

    def __init__(self, project_id: UUID, session: Session):
        self.project_id = project_id
        self.session: Session = session

    def build(self, data: dict) -> Predictor:
        """Build an individual Predictor."""
        predictor: Predictor = Predictor.build(data)
        predictor._session = self.session
        predictor._project_id = self.project_id
        return predictor

    def check_for_update(self, uid: Union[UUID, str] = None,
                         predictor_id: Union[UUID, str] = None) -> Optional[Predictor]:
        """
        Check if there are updates available for a predictor.

        Typically these are updates to the training data. For example, a GEM Table may have
        been re-built to include additional rows.

        This check does not update the predictor; it just returns the update that is available.
        To perform the update, the response should then be used to call PredictorCollection.update

        Parameters
        ----------
        uid: Union[UUID, str]
            Unique identifier of the predictor to check
        predictor_id: Union[UUID, str]
            [DEPRECATED] please use uid instead

        Returns
        -------
        Optional[Predictor]
            The update, if an update is available; None otherwise.

        """
        uid = migrate_deprecated_argument(uid, "uid", predictor_id, "predictor_id")
        path = "/projects/{}/predictors/{}/check-for-update".format(self.project_id, uid)
        data = self.session.get_resource(path)
        if data["updatable"]:
            enveloped = GraphPredictor.stuff_predictor_into_envelope(data["update"])
            built: Predictor = Predictor.build(enveloped)
            built.uid = uid
            return built
        else:
            return None

    def auto_configure(self, *, training_data: DataSource, pattern="PLAIN") -> Predictor:
        """[ALPHA] Create a default predictor for some training data.

        This method will return an unregistered predictor generated by inspecting the
        training data and attempting to automatically configure the predictor.
        The automatic configuration tries to be as inclusive as possible.

        Parameters
        ----------
        training_data: DataSource
            The data to configure the predictor to model.
        pattern: str
            The predictor pattern to use, either "PLAIN" or "FORMULATION"

        Returns
        -------
        Predictor
            Automatically configured predictor for the training data

        """
        if pattern not in {"FORMULATION", "PLAIN"}:
            msg = "Called with pattern: {}.  Expected 'FORMULATION' or 'PLAIN'.".format(pattern)
            raise ValueError(msg)
        path = f'projects/{self.project_id}/predictors/default-predictor'
        body = {"data_source": training_data.dump(), "pattern": pattern}
        data = self.session.post_resource(path, json=body)
        if 'instance' in data:
            data['config'] = data.pop('instance')
        return self.build(data)
