import { useReducer } from "react";

export type DialogState =
  | { type: "close" }
  | { type: "create" }
  | { type: "detail"; id: string }
  | { type: "edit"; id: string }
  | { type: "delete"; id: string };

export type DialogAction =
  | { type: "CLOSE" }
  | { type: "CREATE" }
  | { type: "VIEW_DETAIL"; id: string }
  | { type: "EDIT"; id: string }
  | { type: "DELETE"; id: string };

const defaultInitialState: DialogState = { type: "close" };

const reducer = (state: DialogState, action: DialogAction): DialogState => {
  switch (action.type) {
    case "CLOSE":
      return { type: "close" };
    case "CREATE":
      return { type: "create" };
    case "VIEW_DETAIL":
      return { type: "detail", id: action.id };
    case "EDIT":
      return { type: "edit", id: action.id };
    case "DELETE":
      return { type: "delete", id: action.id };
    default:
      return state;
  }
};

export const useDialogState = (initialState?: DialogState) => {
  const [state, dispatch] = useReducer(
    reducer,
    initialState ?? defaultInitialState
  );

  const setDialogCreate = () => dispatch({ type: "CREATE" });
  const setDialogViewDetail = (id: string) =>
    dispatch({ type: "VIEW_DETAIL", id });
  const setDialogEdit = (id: string) => dispatch({ type: "EDIT", id });
  const setDialogDelete = (id: string) => dispatch({ type: "DELETE", id });
  const setDialogClose = () => dispatch({ type: "CLOSE" });

  return {
    state,
    setDialogCreate,
    setDialogViewDetail,
    setDialogEdit,
    setDialogDelete,
    setDialogClose,
  };
};
